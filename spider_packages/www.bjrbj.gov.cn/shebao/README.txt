#linux ʹ��˵��
# ��װscrapy �Լ�������� 
# �������������������»������û��� ���� PYTHON_SHEBAO_ENV  dev|pro  ���δ���� ��Ĭ��Ϊ dev �˻�������ֻӰ��confs�������ļ���ʹ��
# Ŀǰ�ù�����Ҫ������ ץȡ�����籣������Ϣ  ���ϱ��� ҽ�Ʊ�����Ϣ
  1 scrapy crawl Login -a key=k1    �򿪵�¼��
  2 scrapy crawl VerifyCode -a key=k1  �γ�k1_safe_code.jpg ��֤��ͼƬ
  3 scrapy crawl Info -a key=k1 -a username=���֤�� -a password=ע������ -a safecode=ͼƬ��֤����ֵ  ʹ�õ�һ�����cookie�͵ڶ��������֤�� ��¼ �����籣ץȡ��Ϣ �洢redis
  
#pipelines ����洢��Ϣ ����cookie ������Ϣ �籣�ɷ���Ϣ


#�����Ż����� 
1���� nginx ֱ�ӵ���python 
2�Զ�ʶ�� ��֤�� 
  