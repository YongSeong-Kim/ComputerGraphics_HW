1. 개요
  - 제공받은 스켈레톤 코드로 다음의 기능들을 구현하였습니다.
  1) 소를 클릭하여 움직이면 수평으로 움직이고, 드래그하면 수직으로 움직여서 control point를 지정할 수 있습니다.
  2) control point 6개면 시작점에서 끝점까지 이동합니다.
  3) 끝나는 cow의 위치는 anmation 끝났을떄의 위치입니다. 

수평/수직 드래그 : onMouseButton(), onMouseDrag 편집하여 구현.
	- onMouseButton(), onMouseDrag() 함수를 수정해서 control point를 배열에 넣도록 만들었습니다.
	- onMouseButton() 함수에서 cow의 control point 정보를 배열에 저장하여 관리합니다.
	- onMouseDrag()에서 평면을 x축의 법선 벡터인 평면(y,z평면)으로 만들고 ray와 그 평면이 만나는 점을 계산한 뒤, 계산된 점의 x좌표와 z좌표를 고정시켜서 y좌표값만 변화하게 만들어주었습니다.
	- dragging후 cow의 위치를 선택한후 선택된 곳에서 cow의 drag움직임이 시작할수 있도록 pickInfo를 수정해주는 부분도 vertical drag와 horizontal Drag에 추가해 주었습니다.
	- cow의 숫자를 세서 6개까지 저장하고 그 후 롤러코스터가 실행 됩니다.
	- 롤러코스터가 종료되면 맨 처음 cow의 위치로 cow2wld 돌아가게 됩니다.
	- display() 함수 내부를 편집해서 cow를 구현하였다. 선택된 count_cow의 숫자가 6개 보다 작을때는 그 위치에 cow를 표시하고 6개가 채워지면 computation 함수를 실행해 cow를 그리도록 하였습니다.
	- 시간이 끝나면 cow를 비롯한 전역변수들을 초기화 시켜주고 cow2wld는 이전 cow2wldList의 첫번쨰 index값을 넣어줍니다. 

spline curve를 이용한 cow의 움직임 : display(), computation() 편집하여 구현.
	- catmull-rom 공식을 사용하여 curve를 구현하였습니다.
	- 포인트값은 저장된 cow2wld 행렬의 translate부분(4번째 culumn)만을 따와 사용하였습니다. 
	- 행렬 공식 대입으로 a값에 따른 포인트를 계산하여 cow2wld행렬 4번째 culumn에 대입후 a값에 따라 변화하는 cow2wld를 drawcow()의 인자로 사용 하였습니다.
	- a 값은 get_time()함수를 이용하여 구하고 6초씩 3바퀴를 구현하도록 하였습니다.
	- cow가 움직이는 과정에서 a에 대해 미분하여( 3차 방정식) 그 위치에서의 접선(방향벡터)를 구하였습니다. 
	- a 행렬을 (3a^2, 2a ,1, 0)으로 바꾸고 외적을 이용하여(np.array([3*a*a, 2*a, 1, 0]) @ catmull @ position) normal 변수를 구하였습니다.
	- normal을 이용해 cow의 local 좌표를 구합니다.
	- 결과값을 cow @ y_rotation.T @ np.linalg.inv(mat).T의 연산을 통해 구해 cow를 그려줍니다. 