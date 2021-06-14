Python 3.9.2 (tags/v3.9.2:1a79785, Feb 19 2021, 13:44:55) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from turtle import * # turtle 모듈 불러오기
>>>reset()
>>>shape('turtle')
>>>bgcolor('black') # 배경색상 변경
>>># 함수 - 다양한 색상 도형 만들기
>>>def different_figure(n,angle):
        reset() # 새로운 시작
	speed(0) # 빠르게
	for i in range(n): # 반복함수 만들기 - n(변수)번 반복
		if i % 3 == 0:
			color('red') # 3으로 나눈 나머지가 0이면 색상을 빨간색으로
		if i % 3 == 1:
			color('yellow') # 3으로 나눈 나머지가 1이면 색상을 노란색으로
		if i % 3 == 2:
			color('blue') # 3으로 나눈 나머지가 2이면 색상을 파란색으로
		forward(i * 2) # i * 2 만큼 전진
		left(angle) # angle(변수)만큼 돌기

		
>>># 함수 실행
>>>different_figure(200,29) # 200번 반복, 29도씩 돌기
>>>different_figure(200,59) # 200번 반복, 59도씩 돌기
>>>different_figure(200,89) # 200번 반복, 89도씩 돌기
>>>different_figure(200,119) # 200번 반복, 119도씩 돌기
>>>different_figure(200,149) # 200번 반복, 149도씩 돌기
>>>different_figure(200,179) # 200번 반복, 179도씩 돌기
>>> 
