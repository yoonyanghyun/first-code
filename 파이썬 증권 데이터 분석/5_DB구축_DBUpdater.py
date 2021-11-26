import pandas as pd
import pymysql
from datetime import datetime

class DBUpdater:
    def __init__(self):
        '''생성자: MariaDB 연결 및 종목코드 딕셔너리 생성'''
        self.conn = pymysql.connect(host='localhost', port=3307,user='root',password='1234',db='INVESTAR',charset='utf8')
        # 웹 기반 환경인 colab에서는 접속불가. mariadb가 아닌 mysql이 실행되어있어야 실행가능

        with self.conn.cursor() as curs:
            sql = '''
            CREATE TABLE IF NOT EXISTS company_info(
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            '''
            curs.execute(sql)
            sql = '''
            CREATE TABLE IF NOT EXISTS daily_price(
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            '''
            curs.execute(sql)
        self.conn.commit()

        self.codes = dict()
        self.update_comp_info()
    
    def __del__(self):
        '''소멸자: MariaDB 연결 해제'''
        self.conn.close()
    
    # 종목코드 구하기
    def read_krx_code(self):
        '''KRX로부터 상장법인목록 파일을 읽어와서 데이터프레임으로 반환'''
        krx = pd.read_excel(r'C:\Users\윤양현\Desktop\주식\상장법인목록1.xlsx') # 11월 15일 상장되어있는 상장법인의 종목코드만, 그 이후 상장기업은 적용 x
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'}) # 칼럼 재지정
        krx.code = krx.code.map('{:06d}'.format) # code 형식을 6개의 숫자인 문자열 형식으로 저장
        return krx
    
    # 종목코드를 DB에 업데이트
    def update_comp_info(self):
        '''종목코드를 company_info 테이블에 업데이트한 후 딕셔너리에 저장'''
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx] # codes 딕셔너리 만들기
        with self.conn.cursor() as curs:
            sql = 'SELECT max(last_update) FROM company_info'
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today: # 날짜가 존재하지 않거나, 오늘보다 오래된 경우 업데이트
                krx = self.read_krx_code()
                for idx in range(len(krx)): # krx 종목마다 인덱스 부여
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last_update) VALUES('{code}','{company}','{today}')"
                    curs.execute(sql)
                    self.codes[code] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} REPLACE INTO company_info VALUES ({code}, {company}, {today})")
                self.conn.commit()
                print()

if __name__ == '__main__':        
    dbu = DBUpdater()
    dbu.update_comp_info()