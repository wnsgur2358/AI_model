import pandas as pd  # 데이터 처리를 위한 Pandas 모듈
from flask import Flask, request, jsonify  # Flask 모듈 로드

app = Flask(__name__)  # Flask 애플리케이션 생성

# 음식 데이터를 CSV에서 로드
data = pd.read_csv('food_data.csv')

# 사용자의 입력에 따라 음식 데이터를 필터링하는 함수
def filter_data(food_type, calorie_range, cuisine, protein_important):
    # 음식 타입과 국적을 기준으로 필터링
    filtered_data = data[(data["type"] == food_type) & (data["cuisine"] == cuisine)]

    # 칼로리 범위에 따른 추가 필터링
    if calorie_range == "low":
        filtered_data = filtered_data[filtered_data["calories"] <= 300]
    elif calorie_range == "medium":
        filtered_data = filtered_data[(filtered_data["calories"] > 300) & (filtered_data["calories"] <= 600)]
    else:
        filtered_data = filtered_data[filtered_data["calories"] > 600]

    # 단백질 중요도에 따라 정렬 기준 설정
    if protein_important:
        filtered_data = filtered_data.sort_values(by=["protein", "carbs"], ascending=[False, True])
    else:
        filtered_data = filtered_data.sort_values(by="fat", ascending=True)

    return filtered_data  # 필터링된 데이터 반환

# 추천 API 엔드포인트
@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json  # 클라이언트에서 전달된 JSON 데이터
    # 사용자의 입력 값 추출
    food_type = user_data['foodType']
    calorie_range = user_data['calorieRange']
    cuisine = user_data['cuisine']
    protein_important = user_data['proteinImportant']

    # 필터링된 음식 데이터 반환
    recommendations = filter_data(food_type, calorie_range, cuisine, protein_important)
    return jsonify(recommendations.to_dict(orient='records'))  # 결과를 JSON으로 응답

if __name__ == '__main__':
    app.run(port=5000)  # 서버 실행 (포트 5000)


