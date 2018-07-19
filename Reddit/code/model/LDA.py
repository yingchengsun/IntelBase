'''
Created on Jun 19, 2018

@author: yingc
'''
# _*_ coding: utf-8 _*_

"""
python_lda.py by xianhu
"""

import os
import numpy
import logging
from collections import defaultdict

# ȫ�ֱ���
MAX_ITER_NUM = 10000    # ����������
VAR_NUM = 20            # �Զ������������ʱ,���㷽��������С


class BiDictionary(object):
    """
    ����˫���ֵ�,ͨ��key���Եõ�value,ͨ��valueҲ���Եõ�key
    """

    def __init__(self):
        """
        :key: ˫���ֵ��ʼ��
        """
        self.dict = {}            # ����������ֵ�,��keyΪself��key
        self.dict_reversed = {}   # ����������ֵ�,��keyΪself��value
        return

    def __len__(self):
        """
        :key: ��ȡ˫���ֵ�ĳ���
        """
        return len(self.dict)

    def __str__(self):
        """
        :key: ��˫���ֵ�ת��Ϊ�ַ�������
        """
        str_list = ["%s\t%s" % (key, self.dict[key]) for key in self.dict]
        return "\n".join(str_list)

    def clear(self):
        """
        :key: ���˫���ֵ����
        """
        self.dict.clear()
        self.dict_reversed.clear()
        return

    def add_key_value(self, key, value):
        """
        :key: ����˫���ֵ�,����һ��
        """
        self.dict[key] = value
        self.dict_reversed[value] = key
        return

    def remove_key_value(self, key, value):
        """
        :key: ����˫���ֵ�,ɾ��һ��
        """
        if key in self.dict:
            del self.dict[key]
            del self.dict_reversed[value]
        return

    def get_value(self, key, default=None):
        """
        :key: ͨ��key��ȡvalue,�����ڷ���default
        """
        return self.dict.get(key, default)

    def get_key(self, value, default=None):
        """
        :key: ͨ��value��ȡkey,�����ڷ���default
        """
        return self.dict_reversed.get(value, default)

    def contains_key(self, key):
        """
        :key: �ж��Ƿ����keyֵ
        """
        return key in self.dict

    def contains_value(self, value):
        """
        :key: �ж��Ƿ����valueֵ
        """
        return value in self.dict_reversed

    def keys(self):
        """
        :key: �õ�˫���ֵ�ȫ����keys
        """
        return self.dict.keys()

    def values(self):
        """
        :key: �õ�˫���ֵ�ȫ����values
        """
        return self.dict_reversed.keys()

    def items(self):
        """
        :key: �õ�˫���ֵ�ȫ����items
        """
        return self.dict.items()


class CorpusSet(object):
    """
    �������ϼ���,��ΪLdaBase�Ļ���
    """

    def __init__(self):
        """
        :key: ��ʼ������
        """
        # �������word�ı���
        self.local_bi = BiDictionary()      # id��word֮��ı���˫���ֵ�,keyΪid,valueΪword
        self.words_count = 0                # ���ݼ���word������������֮ǰ�ģ�
        self.V = 0                          # ���ݼ���word������������֮��ģ�

        # �������article�ı���
        self.artids_list = []               # ȫ��article��id���б�,�������ݶ�ȡ��˳��洢
        self.arts_Z = []                    # ȫ��article�����дʵ�id��Ϣ,ά��Ϊ M * art.length()
        self.M = 0                          # ���ݼ���article������

        # �����ƶ����õ��ı���������Ϊ�գ�
        self.global_bi = None               # id��word֮���ȫ��˫���ֵ�,keyΪid,valueΪword
        self.local_2_global = {}            # һ���ֵ�,local�ֵ��global�ֵ�֮��Ķ�Ӧ��ϵ
        return

    def init_corpus_with_file(self, file_name):
        """
        :key: ���������ļ���ʼ�����ϼ����ݡ��ļ�ÿһ�е����ݸ�ʽ: id[tab]word1 word2 word3......
        """
        with open(file_name, "r", encoding="utf-8") as file_iter:
            self.init_corpus_with_articles(file_iter)
        return

    def init_corpus_with_articles(self, article_list):
        """
        :key: ����article���б��ʼ�����ϼ���ÿһƪarticle�ĸ�ʽΪ: id[tab]word1 word2 word3......
        """
        # ��������--word����
        self.local_bi.clear()
        self.words_count = 0
        self.V = 0

        # ��������--article����
        self.artids_list.clear()
        self.arts_Z.clear()
        self.M = 0

        # ��������--����local��global��ӳ���ϵ
        self.local_2_global.clear()

        # ��ȡarticle����
        for line in article_list:
            frags = line.strip().split()
            if len(frags) < 2:
                continue

            # ��ȡarticle��id
            art_id = frags[0].strip()

            # ��ȡword��id
            art_wordid_list = []
            for word in [w.strip() for w in frags[1:] if w.strip()]:
                local_id = self.local_bi.get_key(word) if self.local_bi.contains_value(word) else len(self.local_bi)

                # �����self.global_biΪNone��Ϊ�����������
                if self.global_bi is None:
                    # ����id��Ϣ
                    self.local_bi.add_key_value(local_id, word)
                    art_wordid_list.append(local_id)
                else:
                    if self.global_bi.contains_value(word):
                        # ����id��Ϣ
                        self.local_bi.add_key_value(local_id, word)
                        art_wordid_list.append(local_id)

                        # ����local_2_global
                        self.local_2_global[local_id] = self.global_bi.get_key(word)

            # ���������: ����article��word����������0
            if len(art_wordid_list) > 0:
                self.words_count += len(art_wordid_list)
                self.artids_list.append(art_id)
                self.arts_Z.append(art_wordid_list)

        # ����س�ʼ����--word���
        self.V = len(self.local_bi)
        logging.debug("words number: " + str(self.V) + ", " + str(self.words_count))

        # ����س�ʼ����--article���
        self.M = len(self.artids_list)
        logging.debug("articles number: " + str(self.M))
        return

    def save_wordmap(self, file_name):
        """
        :key: ����word�ֵ�,��self.local_bi������
        """
        with open(file_name, "w", encoding="utf-8") as f_save:
            f_save.write(str(self.local_bi))
        return

    def load_wordmap(self, file_name):
        """
        :key: ����word�ֵ�,������self.local_bi������
        """
        self.local_bi.clear()
        with open(file_name, "r", encoding="utf-8") as f_load:
            for _id, _word in [line.strip().split() for line in f_load if line.strip()]:
                self.local_bi.add_key_value(int(_id), _word.strip())
        self.V = len(self.local_bi)
        return


class LdaBase(CorpusSet):
    """
    LDAģ�͵Ļ���,���˵��:
    ��article���±귶ΧΪ[0, self.M), �±�Ϊ m
    ��wordid���±귶ΧΪ[0, self.V), �±�Ϊ w
    ��topic���±귶ΧΪ[0, self.K), �±�Ϊ k �� topic
    ��article��word���±귶ΧΪ[0, article.size()), �±�Ϊ n
    """

    def __init__(self):
        """
        :key: ��ʼ������
        """
        CorpusSet.__init__(self)

        # ��������--1
        self.dir_path = ""          # �ļ���·��,���ڴ��LDA���е����ݡ��м�����
        self.model_name = ""        # LDAѵ�����ƶϵ�ģ������,Ҳ���ڶ�ȡѵ���Ľ��
        self.current_iter = 0       # LDAѵ�����ƶϵ�ģ���Ѿ������Ĵ���,���ڼ���ģ��ѵ������
        self.iters_num = 0          # LDAѵ�����ƶϹ�����Gibbs�����������ܴ���,����ֵ����"auto"
        self.topics_num = 0         # LDAѵ�����ƶϹ����е�topic������,��self.Kֵ
        self.K = 0                  # LDAѵ�����ƶϹ����е�topic������,��self.topics_numֵ
        self.twords_num = 0         # LDAѵ�����ƶϽ����������ÿ��topic��ص�word�ĸ���

        # ��������--2
        self.alpha = numpy.zeros(self.K)            # ������alpha,Kά��floatֵ,Ĭ��Ϊ50/K
        self.beta = numpy.zeros(self.V)             # ������beta,Vά��floatֵ,Ĭ��Ϊ0.01

        # ��������--3
        self.Z = []                                 # ����word��topic��Ϣ,��Z(m, n),ά��Ϊ M * article.size()

        # ͳ�Ƽ���(����self.Z����õ�)
        self.nd = numpy.zeros((self.M, self.K))     # nd[m, k]���ڱ����mƪarticle�е�k��topic�����Ĵʵĸ���,��ά��Ϊ M * K
        self.ndsum = numpy.zeros((self.M, 1))       # ndsum[m, 0]���ڱ����mƪarticle���ܴ���,ά��Ϊ M * 1
        self.nw = numpy.zeros((self.K, self.V))     # nw[k, w]���ڱ����k��topic�����Ĵ��е�w���ʵ�����,��ά��Ϊ K * V
        self.nwsum = numpy.zeros((self.K, 1))       # nwsum[k, 0]���ڱ����k��topic�����Ĵʵ�����,ά��Ϊ K * 1

        # ����ʽ�ֲ���������
        self.theta = numpy.zeros((self.M, self.K))  # Doc-Topic����ʽ�ֲ��Ĳ���,ά��Ϊ M * K,��alphaֵӰ��
        self.phi = numpy.zeros((self.K, self.V))    # Topic-Word����ʽ�ֲ��Ĳ���,ά��Ϊ K * V,��betaֵӰ��

        # ��������,Ŀ��������㷨ִ��Ч��
        self.sum_alpha = 0.0                        # ������alpha�ĺ�
        self.sum_beta = 0.0                         # ������beta�ĺ�

        # ����֪ʶ,��ʽΪ{word_id: [k1, k2, ...], ...}
        self.prior_word = defaultdict(list)

        # �ƶ�ʱ��Ҫ��ѵ��ģ��
        self.train_model = None
        return

    # --------------------------------------------------��������---------------------------------------------------------
    def init_statistics_document(self):
        """
        :key: ��ʼ������article��ͳ�Ƽ������Ⱦ�����: self.M, self.K, self.Z
        """
        assert self.M > 0 and self.K > 0 and self.Z

        # ͳ�Ƽ�����ʼ��
        self.nd = numpy.zeros((self.M, self.K), dtype=numpy.int)
        self.ndsum = numpy.zeros((self.M, 1), dtype=numpy.int)

        # ����self.Z���и���,����self.nd[m, k]��self.ndsum[m, 0]
        for m in range(self.M):
            for k in self.Z[m]:
                self.nd[m, k] += 1
            self.ndsum[m, 0] = len(self.Z[m])
        return

    def init_statistics_word(self):
        """
        :key: ��ʼ������word��ͳ�Ƽ������Ⱦ�����: self.V, self.K, self.Z, self.arts_Z
        """
        assert self.V > 0 and self.K > 0 and self.Z and self.arts_Z

        # ͳ�Ƽ�����ʼ��
        self.nw = numpy.zeros((self.K, self.V), dtype=numpy.int)
        self.nwsum = numpy.zeros((self.K, 1), dtype=numpy.int)

        # ����self.Z���и���,����self.nw[k, w]��self.nwsum[k, 0]
        for m in range(self.M):
            for k, w in zip(self.Z[m], self.arts_Z[m]):
                self.nw[k, w] += 1
                self.nwsum[k, 0] += 1
        return

    def init_statistics(self):
        """
        :key: ��ʼ��ȫ����ͳ�Ƽ������������������ۺϺ�����
        """
        self.init_statistics_document()
        self.init_statistics_word()
        return

    def sum_alpha_beta(self):
        """
        :key: ����alpha��beta�ĺ�
        """
        self.sum_alpha = self.alpha.sum()
        self.sum_beta = self.beta.sum()
        return

    def calculate_theta(self):
        """
        :key: ��ʼ��������ģ�͵�thetaֵ(M*K),�õ�alphaֵ
        """
        assert self.sum_alpha > 0
        self.theta = (self.nd + self.alpha) / (self.ndsum + self.sum_alpha)
        return

    def calculate_phi(self):
        """
        :key: ��ʼ��������ģ�͵�phiֵ(K*V),�õ�betaֵ
        """
        assert self.sum_beta > 0
        self.phi = (self.nw + self.beta) / (self.nwsum + self.sum_beta)
        return

    # ---------------------------------------------����Perplexityֵ------------------------------------------------------
    def calculate_perplexity(self):
        """
        :key: ����Perplexityֵ,������
        """
        # ����theta��phiֵ
        self.calculate_theta()
        self.calculate_phi()

        # ��ʼ����
        preplexity = 0.0
        for m in range(self.M):
            for w in self.arts_Z[m]:
                preplexity += numpy.log(numpy.sum(self.theta[m] * self.phi[:, w]))
        return numpy.exp(-(preplexity / self.words_count))

    # --------------------------------------------------��̬����---------------------------------------------------------
    @staticmethod
    def multinomial_sample(pro_list):
        """
        :key: ��̬����,����ʽ�ֲ�����,��ʱ��ı�pro_list��ֵ
        :param pro_list: [0.2, 0.7, 0.4, 0.1],��ʱ˵�������±�1�Ŀ����Դ�,��Ҳ������
        """
        # ��pro_list�����ۼ�
        for k in range(1, len(pro_list)):
            pro_list[k] += pro_list[k-1]

        # ȷ������� u �����ĸ��±�ֵ,��ʱ���±�ֵ��Ϊ��ȡ�����random.rand()����: [0, 1.0)��
        u = numpy.random.rand() * pro_list[-1]

        return_index = len(pro_list) - 1
        for t in range(len(pro_list)):
            if pro_list[t] > u:
                return_index = t
                break
        return return_index

    # ----------------------------------------------Gibbs�����㷨--------------------------------------------------------
    def gibbs_sampling(self, is_calculate_preplexity):
        """
        :key: LDAģ���е�Gibbs��������
        :param is_calculate_preplexity: �Ƿ����preplexityֵ
        """
        # ����preplexityֵ�õ��ı���
        pp_list = []
        pp_var = numpy.inf

        # ��ʼ����
        last_iter = self.current_iter + 1
        iters_num = self.iters_num if self.iters_num != "auto" else MAX_ITER_NUM
        for self.current_iter in range(last_iter, last_iter+iters_num):
            info = "......"

            # �Ƿ����preplexityֵ
            if is_calculate_preplexity:
                pp = self.calculate_perplexity()
                pp_list.append(pp)

                # �����б�����VAR_NUM��ķ���
                pp_var = numpy.var(pp_list[-VAR_NUM:]) if len(pp_list) >= VAR_NUM else numpy.inf
                info = (", preplexity: " + str(pp)) + ((", var: " + str(pp_var)) if len(pp_list) >= VAR_NUM else "")

            # ���Debug��Ϣ
            logging.debug("\titeration " + str(self.current_iter) + info)

            # �ж��Ƿ�����ѭ��
            if self.iters_num == "auto" and pp_var < (VAR_NUM / 2):
                break

            # ��ÿƪarticle��ÿ��word����һ�γ���,��ȡ���ʵ�kֵ
            for m in range(self.M):
                for n in range(len(self.Z[m])):
                    w = self.arts_Z[m][n]
                    k = self.Z[m][n]

                    # ͳ�Ƽ�����һ
                    self.nd[m, k] -= 1
                    self.ndsum[m, 0] -= 1
                    self.nw[k, w] -= 1
                    self.nwsum[k, 0] -= 1

                    if self.prior_word and (w in self.prior_word):
                        # ��������֪ʶ,���������������
                        k = numpy.random.choice(self.prior_word[w])
                    else:
                        # ����thetaֵ--�±ߵĹ���Ϊ��ȡ��mƪarticle�ĵ�n����w��topic,���µ�k
                        theta_p = (self.nd[m] + self.alpha) / (self.ndsum[m, 0] + self.sum_alpha)

                        # ����phiֵ--�ж���ѵ��ģ��,�����ƶ�ģ�ͣ�ע��self.beta[w_g]��
                        if self.local_2_global and self.train_model:
                            w_g = self.local_2_global[w]
                            phi_p = (self.train_model.nw[:, w_g] + self.nw[:, w] + self.beta[w_g]) / \
                                    (self.train_model.nwsum[:, 0] + self.nwsum[:, 0] + self.sum_beta)
                        else:
                            phi_p = (self.nw[:, w] + self.beta[w]) / (self.nwsum[:, 0] + self.sum_beta)

                        # multi_pΪ����ʽ�ֲ��Ĳ���,��ʱû�н��б�׼��
                        multi_p = theta_p * phi_p

                        # ��ʱ��topic��ΪGibbs�����õ���topic,���нϴ�ĸ������ж���ʽ���ʴ��topic
                        k = LdaBase.multinomial_sample(multi_p)

                    # ͳ�Ƽ�����һ
                    self.nd[m, k] += 1
                    self.ndsum[m, 0] += 1
                    self.nw[k, w] += 1
                    self.nwsum[k, 0] += 1

                    # ����Zֵ
                    self.Z[m][n] = k
        # �������
        return

    # -----------------------------------------Model���ݴ洢����ȡ��غ���-------------------------------------------------
    def save_parameter(self, file_name):
        """
        :key: ����ģ����ز�������,����: topics_num, M, V, K, words_count, alpha, beta
        """
        with open(file_name, "w", encoding="utf-8") as f_param:
            for item in ["topics_num", "M", "V", "K", "words_count"]:
                f_param.write("%s\t%s\n" % (item, str(self.__dict__[item])))
            f_param.write("alpha\t%s\n" % ",".join([str(item) for item in self.alpha]))
            f_param.write("beta\t%s\n" % ",".join([str(item) for item in self.beta]))
        return

    def load_parameter(self, file_name):
        """
        :key: ����ģ����ز�������,����һ���������Ӧ
        """
        with open(file_name, "r", encoding="utf-8") as f_param:
            for line in f_param:
                key, value = line.strip().split()
                if key in ["topics_num", "M", "V", "K", "words_count"]:
                    self.__dict__[key] = int(value)
                elif key in ["alpha", "beta"]:
                    self.__dict__[key] = numpy.array([float(item) for item in value.split(",")])
        return

    def save_zvalue(self, file_name):
        """
        :key: ����ģ�͹���article�ı���,����: arts_Z, Z, artids_list��
        """
        with open(file_name, "w", encoding="utf-8") as f_zvalue:
            for m in range(self.M):
                out_line = [str(w) + ":" + str(k) for w, k in zip(self.arts_Z[m], self.Z[m])]
                f_zvalue.write(self.artids_list[m] + "\t" + " ".join(out_line) + "\n")
        return

    def load_zvalue(self, file_name):
        """
        :key: ��ȡģ�͵�Z����������һ���������Ӧ
        """
        self.arts_Z = []
        self.artids_list = []
        self.Z = []
        with open(file_name, "r", encoding="utf-8") as f_zvalue:
            for line in f_zvalue:
                frags = line.strip().split()
                art_id = frags[0].strip()
                w_k_list = [value.split(":") for value in frags[1:]]
                # ��ӵ�����
                self.artids_list.append(art_id)
                self.arts_Z.append([int(item[0]) for item in w_k_list])
                self.Z.append([int(item[1]) for item in w_k_list])
        return

    def save_twords(self, file_name):
        """
        :key: ����ģ�͵�twords����,Ҫ�õ�phi������
        """
        self.calculate_phi()
        out_num = self.V if self.twords_num > self.V else self.twords_num
        with open(file_name, "w", encoding="utf-8") as f_twords:
            for k in range(self.K):
                words_list = sorted([(w, self.phi[k, w]) for w in range(self.V)], key=lambda x: x[1], reverse=True)
                f_twords.write("Topic %dth:\n" % k)
                f_twords.writelines(["\t%s %f\n" % (self.local_bi.get_value(w), p) for w, p in words_list[:out_num]])
        return

    def load_twords(self, file_name):
        """
        :key: ����ģ�͵�twords����,����������
        """
        self.prior_word.clear()
        topic = -1
        with open(file_name, "r", encoding="utf-8") as f_twords:
            for line in f_twords:
                if line.startswith("Topic"):
                    topic = int(line.strip()[6:-3])
                else:
                    word_id = self.local_bi.get_key(line.strip().split()[0].strip())
                    self.prior_word[word_id].append(topic)
        return

    def save_tag(self, file_name):
        """
        :key: ���ģ�����ո����ݴ��ǩ�Ľ��,�õ�thetaֵ
        """
        self.calculate_theta()
        with open(file_name, "w", encoding="utf-8") as f_tag:
            for m in range(self.M):
                f_tag.write("%s\t%s\n" % (self.artids_list[m], " ".join([str(item) for item in self.theta[m]])))
        return

    def save_model(self):
        """
        :key: ����ģ������
        """
        name_predix = "%s-%05d" % (self.model_name, self.current_iter)

        # ����ѵ�����
        self.save_parameter(os.path.join(self.dir_path, "%s.%s" % (name_predix, "param")))
        self.save_wordmap(os.path.join(self.dir_path, "%s.%s" % (name_predix, "wordmap")))
        self.save_zvalue(os.path.join(self.dir_path, "%s.%s" % (name_predix, "zvalue")))

        #�����������
        self.save_twords(os.path.join(self.dir_path, "%s.%s" % (name_predix, "twords")))
        self.save_tag(os.path.join(self.dir_path, "%s.%s" % (name_predix, "tag")))
        return

    def load_model(self):
        """
        :key: ����ģ������
        """
        name_predix = "%s-%05d" % (self.model_name, self.current_iter)

        # ����ѵ�����
        self.load_parameter(os.path.join(self.dir_path, "%s.%s" % (name_predix, "param")))
        self.load_wordmap(os.path.join(self.dir_path, "%s.%s" % (name_predix, "wordmap")))
        self.load_zvalue(os.path.join(self.dir_path, "%s.%s" % (name_predix, "zvalue")))
        return


class LdaModel(LdaBase):
    """
    LDAģ�Ͷ���,��Ҫʵ��ѵ��������ѵ�����ƶϵĹ���
    """

    def init_train_model(self, dir_path, model_name, current_iter, iters_num=None, topics_num=10, twords_num=200,
                         alpha=-1.0, beta=0.01, data_file="", prior_file=""):
        """
        :key: ��ʼ��ѵ��ģ��,���ݲ���current_iter���Ƿ����0�������ǳ�ʼ����ģ��,���Ǽ�������ģ��
        :key: ����ʼ����ģ��ʱ,����prior_file�����ļ���,�������еĲ�������Ҫ,��current_iter����0
        :key: ����������ģ��ʱ,ֻ��Ҫdir_path, model_name, current_iter��������0��, iters_num, twords_num����
        :param iters_num: ����Ϊ����ֵ���ߡ�auto��
        """
        if current_iter == 0:
            logging.debug("init a new train model")

            # ��ʼ�����ϼ�
            self.init_corpus_with_file(data_file)

            # ��ʼ�����ֱ���
            self.dir_path = dir_path
            self.model_name = model_name
            self.current_iter = current_iter
            self.iters_num = iters_num
            self.topics_num = topics_num
            self.K = topics_num
            self.twords_num = twords_num

            # ��ʼ��alpha��beta
            self.alpha = numpy.array([alpha if alpha > 0 else (50.0/self.K) for k in range(self.K)])
            self.beta = numpy.array([beta if beta > 0 else 0.01 for w in range(self.V)])

            # ��ʼ��Zֵ,�Ա�ͳ�Ƽ���
            self.Z = [[numpy.random.randint(self.K) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]
        else:
            logging.debug("init an existed model")

            # ��ʼ�����ֱ���
            self.dir_path = dir_path
            self.model_name = model_name
            self.current_iter = current_iter
            self.iters_num = iters_num
            self.twords_num = twords_num

            # ��������ģ��
            self.load_model()

        # ��ʼ��ͳ�Ƽ���
        self.init_statistics()

        # ����alpha��beta�ĺ�ֵ
        self.sum_alpha_beta()

        # ��ʼ������֪ʶ
        if prior_file:
            self.load_twords(prior_file)

        # ���ظ�ģ��
        return self

    def begin_gibbs_sampling_train(self, is_calculate_preplexity=True):
        """
        :key: ѵ��ģ��,�����ϼ��е��������ݽ���Gibbs����,���������ĳ������
        """
        # Gibbs����
        logging.debug("sample iteration start, iters_num: " + str(self.iters_num))
        self.gibbs_sampling(is_calculate_preplexity)
        logging.debug("sample iteration finish")

        # ����ģ��
        logging.debug("save model")
        self.save_model()
        return

    def init_inference_model(self, train_model):
        """
        :key: ��ʼ���ƶ�ģ��
        """
        self.train_model = train_model

        # ��ʼ������: ��Ҫ�õ�self.topics_num, self.K
        self.topics_num = train_model.topics_num
        self.K = train_model.K

        # ��ʼ������self.alpha, self.beta,ֱ������train_model��ֵ
        self.alpha = train_model.alpha      # Kά��floatֵ,ѵ�����ƶ�ģ���е�K��ͬ,�ʿ�������
        self.beta = train_model.beta        # Vά��floatֵ,�ƶ�ģ�������ڼ���phi��VֵӦ����ȫ�ֵ�word������,�ʿ�������
        self.sum_alpha_beta()               # ����alpha��beta�ĺ�

        # ��ʼ�����ݼ���self.global_bi
        self.global_bi = train_model.local_bi
        return

    def inference_data(self, article_list, iters_num=100, repeat_num=3):
        """
        :key: ��������ģ���ƶ�����
        :param article_list: ÿһ�е����ݸ�ʽΪ: id[tab]word1 word2 word3......
        :param iters_num: ÿһ�ε����Ĵ���
        :param repeat_num: �ظ������Ĵ���
        """
        # ��ʼ�����ϼ�
        self.init_corpus_with_articles(article_list)

        # ��ʼ�����ر���
        return_theta = numpy.zeros((self.M, self.K))

        # �ظ�����
        for i in range(repeat_num):
            logging.debug("inference repeat_num: " + str(i+1))

            # ��ʼ������
            self.current_iter = 0
            self.iters_num = iters_num

            # ��ʼ��Zֵ,�Ա�ͳ�Ƽ���
            self.Z = [[numpy.random.randint(self.K) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]

            # ��ʼ��ͳ�Ƽ���
            self.init_statistics()

            # ��ʼ�ƶ�
            self.gibbs_sampling(is_calculate_preplexity=False)

            # ����theta
            self.calculate_theta()
            return_theta += self.theta

        # ������,������
        return return_theta / repeat_num


if __name__ == "__main__":
    """
    ���Դ���
    """
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

    # train����inference
    test_type = "train"
    # test_type = "inference"

    # ������ģ��
    if test_type == "train":
        model = LdaModel()
        # ��prior_file�����Ƿ��������֪ʶ
        model.init_train_model("data/", "model", current_iter=0, iters_num="auto", topics_num=10, data_file="corpus.txt")
        # model.init_train_model("data/", "model", current_iter=0, iters_num="auto", topics_num=10, data_file="corpus.txt", prior_file="prior.twords")
        model.begin_gibbs_sampling_train()
    elif test_type == "inference":
        model = LdaModel()
        model.init_inference_model(LdaModel().init_train_model("data/", "model", current_iter=134))
        data = [
            "cn    �乾 ���� �乾 ���� ���� ���� �乾 ���� ��Դ ͵�� ���� ȫ�� ���� ʵʱ ���߿� �������� ��½ ���� ��Դ �ڰ� ȫ�� ������",
            "co    aircloud aircloud Ӳ�� �豸 wifi ���� ��Ҫ ƽ����� ���� �洢 aircloud �ļ� Զ�� �ͺ� aircloud Ӳ�� �豸 wifi"
        ]
        result = model.inference_data(data)

    # �˳�����
    exit()