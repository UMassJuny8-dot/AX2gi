import streamlit as st

# 페이지 설정
st.set_page_config(page_title="무역직무 MBTI 테스트", page_icon="🚢", layout="centered")

st.title("🚢 무역마스터: 나의 무역직무 MBTI 테스트")
st.write("20개의 질문을 통해 나의 성향에 가장 잘 맞는 무역 직무를 알아보세요!")
st.markdown("---")

# 20개 질문 리스트 (E/I, S/N, T/F, J/P 각각 5문항)
questions = [
    {"id": "E/I_1", "text": "1. 새로운 바이어를 만나는 네트워킹 자리에서 나는?", "choices": {"적극적으로 명함을 건네며 대화를 주도한다.": "E", "조용히 상황을 파악하며 1:1 대화에 집중한다.": "I"}},
    {"id": "E/I_2", "text": "2. 업무 중 스트레스를 풀 때 나는?", "choices": {"팀원들과 회식을 하거나 수다를 떤다.": "E", "혼자 조용히 휴식을 취한다.": "I"}},
    {"id": "E/I_3", "text": "3. 해외 출장이 잡혔을 때 내 기분은?", "choices": {"새로운 사람과 환경을 만날 생각에 신난다.": "E", "낯선 환경에 적응할 생각에 조금 부담된다.": "I"}},
    {"id": "E/I_4", "text": "4. 회의 중 의견을 낼 때 나는?", "choices": {"생각나는 대로 바로바로 말한다.": "E", "생각을 충분히 정리한 후 발언한다.": "I"}},
    {"id": "E/I_5", "text": "5. 팀 프로젝트를 할 때 선호하는 방식은?", "choices": {"다 같이 모여서 활발하게 브레인스토밍한다.": "E", "각자 역할을 나누고 개인적으로 작업 후 취합한다.": "I"}},
    
    {"id": "S/N_1", "text": "6. 무역 서류(B/L, L/C 등)를 검토할 때 나는?", "choices": {"꼼꼼하게 오탈자와 숫자를 확인한다.": "S", "전체적인 흐름과 거래의 큰 그림을 본다.": "N"}},
    {"id": "S/N_2", "text": "7. 신규 시장을 개척할 때 선호하는 접근은?", "choices": {"과거 판매 데이터와 확실한 통계를 분석한다.": "S", "앞으로의 트렌드와 미래 성장 가능성을 상상한다.": "N"}},
    {"id": "S/N_3", "text": "8. 업무 매뉴얼을 대할 때 나는?", "choices": {"매뉴얼에 적힌 순서대로 정확하게 처리한다.": "S", "매뉴얼을 참고하되 더 효율적인 나만의 방식을 찾는다.": "N"}},
    {"id": "S/N_4", "text": "9. 문제가 발생했을 때(예: 운송 지연) 해결 방식은?", "choices": {"현재 상황에서 즉각적이고 현실적인 대안을 찾는다.": "S", "왜 이런 일이 생겼는지 근본적인 원인과 장기적 대책을 고민한다.": "N"}},
    {"id": "S/N_5", "text": "10. 제품 설명서를 바이어에게 전달할 때 나는?", "choices": {"제품의 정확한 스펙과 성능 위주로 설명한다.": "S", "제품이 가져다줄 혁신적인 가치와 비전을 강조한다.": "N"}},
    
    {"id": "T/F_1", "text": "11. 바이어가 무리한 단가 인하를 요구할 때 나는?", "choices": {"원가와 마진율을 논리적으로 제시하며 거절한다.": "T", "바이어의 입장에 공감하며 원만하게 타협점을 찾는다.": "F"}},
    {"id": "T/F_2", "text": "12. 팀원이 치명적인 업무 실수를 했을 때 나의 첫 마디는?", "choices": {"'어떻게 된 일이야? 해결책은 뭐야?'": "T", "'괜찮아? 많이 당황했겠다.'": "F"}},
    {"id": "T/F_3", "text": "13. 거래처와 협상할 때 가장 중요하게 생각하는 것은?", "choices": {"우리 회사의 이익과 명확한 계약 조건": "T", "거래처와의 긍정적인 관계 유지와 상호 신뢰": "F"}},
    {"id": "T/F_4", "text": "14. 성과 평가를 받을 때 내가 원하는 피드백은?", "choices": {"객관적인 데이터와 실적에 기반한 평가": "T", "나의 노력과 팀에 기여한 과정에 대한 인정": "F"}},
    {"id": "T/F_5", "text": "15. 고객 클레임이 들어왔을 때 대처 방식은?", "choices": {"계약서 조항과 사실 관계를 먼저 따진다.": "T", "고객의 화난 감정을 먼저 누그러뜨리고 사과한다.": "F"}},
    
    {"id": "J/P_1", "text": "16. 한 달 일정의 대형 선적 프로젝트를 맡았다면?", "choices": {"일자별로 세부 일정을 짜고 철저히 지킨다.": "J", "큰 기한만 정해두고 상황에 맞게 유동적으로 대처한다.": "P"}},
    {"id": "J/P_2", "text": "17. 퇴근 직전 긴급한 이메일 회신 요청이 들어왔을 때?", "choices": {"빨리 마무리하고 원래 계획된 퇴근을 한다.": "J", "어쩔 수 없지 하며 남아서 유연하게 처리한다.": "P"}},
    {"id": "J/P_3", "text": "18. 내 사무실 책상의 상태는 보통 어떤가?", "choices": {"필요한 서류와 물품이 각 잡혀 정리되어 있다.": "J", "어수선해 보이지만 나름의 규칙으로 찾을 수 있다.": "P"}},
    {"id": "J/P_4", "text": "19. 해외 출장 짐을 쌀 때 나는?", "choices": {"며칠 전부터 체크리스트를 만들어 완벽하게 싼다.": "J", "출발 전날 닥쳐서 필요한 것들을 생각나는 대로 넣는다.": "P"}},
    {"id": "J/P_5", "text": "20. 돌발 상황(선박 스케줄 지연 등)이 발생했을 때 나는?", "choices": {"계획이 틀어진 것에 크게 스트레스를 받는다.": "J", "'그럴 수도 있지' 하며 즉흥적으로 대안을 찾는다.": "P"}},
]

# 6개 무역 직무 매칭 사전
trade_roles = {
    "해외영업 (Overseas Sales)": {
        "mbti": ["ESTJ", "ENTJ", "ENFJ", "ESTP"],
        "desc": "강한 추진력과 사교성으로 해외 바이어를 발굴하고 수출 계약을 성사시키는 최전선의 전사입니다."
    },
    "무역사무 및 서류 (Trade Documentation)": {
        "mbti": ["ISTJ", "ISFJ"],
        "desc": "B/L, L/C 등 복잡한 무역 서류를 오차 없이 처리하며 꼼꼼함과 책임감으로 백오피스를 든든하게 지킵니다."
    },
    "물류/SCM 관리 (Logistics/SCM)": {
        "mbti": ["ISTP", "ISFP", "ESFJ"],
        "desc": "제품이 출발지에서 목적지까지 안전하게 도착하도록 운송 스케줄과 물류 비용을 효율적으로 통제합니다."
    },
    "해외마케팅 (Overseas Marketing)": {
        "mbti": ["ENFP", "ENTP", "INFJ"],
        "desc": "창의적인 아이디어와 트렌드 분석을 통해 글로벌 시장에서 자사 제품의 매력을 극대화합니다."
    },
    "무역 규제 및 통관 (Customs/Compliance)": {
        "mbti": ["INTJ", "INTP"],
        "desc": "각국의 복잡한 FTA, 관세법, 수출입 규제를 깊이 있게 분석하여 기업의 법적 리스크를 최소화합니다."
    },
    "소싱 및 구매 (Sourcing/Purchasing)": {
        "mbti": ["ESFP", "INFP"],
        "desc": "글로벌 공급망에서 경쟁력 있는 단가로 우수한 제품을 찾아내고, 공급처와 유연하게 협력합니다."
    }
}

# 사용자 응답 저장 딕셔너리
responses = {}

with st.form("mbti_form"):
    for q in questions:
        # Streamlit radio 버튼 생성
        answer = st.radio(q["text"], list(q["choices"].keys()), index=None)
        if answer:
            responses[q["id"]] = q["choices"][answer]
        st.write("") 
    
    submitted = st.form_submit_button("결과 보기")

if submitted:
    if len(responses) < 20:
        st.warning("모든 질문에 답해주세요!")
    else:
        # MBTI 계산
        scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        for val in responses.values():
            scores[val] += 1
            
        mbti_result = ""
        mbti_result += "E" if scores["E"] >= scores["I"] else "I"
        mbti_result += "S" if scores["S"] >= scores["N"] else "N"
        mbti_result += "T" if scores["T"] >= scores["F"] else "F"
        mbti_result += "J" if scores["J"] >= scores["P"] else "P"
        
        st.success(f"당신의 MBTI는 **{mbti_result}** 입니다!")
        
        # 직무 매칭
        matched_role = None
        for role, data in trade_roles.items():
            if mbti_result in data["mbti"]:
                matched_role = (role, data["desc"])
                break
        
        # 예외 처리 (매칭되지 않은 성향은 가장 유사한 직무로 임의 할당)
        if not matched_role:
             matched_role = ("해외영업 (Overseas Sales)", trade_roles["해외영업 (Overseas Sales)"]["desc"])

        st.markdown("### 🏆 추천 무역 직무")
        st.info(f"**{matched_role[0]}**")
        st.write(matched_role[1])
        st.balloons()