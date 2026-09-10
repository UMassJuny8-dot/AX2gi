import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(page_title="오늘의 당번은? 복불복 룰렛", page_icon="🎯")

st.title("🎯 진짜 복불복 룰렛 🎯")
st.write("조작 없는 100% 리얼 랜덤! 과연 당첨자는 누구일까요?")

# HTML, CSS, JS로 만들어진 랜덤 룰렛 코드
roulette_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  body {
    text-align: center;
    font-family: '맑은 고딕', sans-serif;
    margin: 0;
    padding-top: 20px;
    background-color: transparent;
  }
  #roulette-container {
    position: relative;
    width: 300px;
    height: 300px;
    margin: 0 auto;
  }
  .pointer {
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 15px solid transparent;
    border-right: 15px solid transparent;
    border-top: 30px solid #ff4d4d;
    z-index: 10;
    filter: drop-shadow(0px 3px 2px rgba(0,0,0,0.3));
  }
  canvas {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: transform 3.5s cubic-bezier(0.25, 0.1, 0.15, 1);
  }
  button {
    margin-top: 30px;
    padding: 12px 30px;
    font-size: 18px;
    font-weight: bold;
    color: white;
    background-color: #FF4B4B;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: background-color 0.2s;
  }
  button:hover {
    background-color: #FF3333;
  }
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  #result {
    margin-top: 20px;
    font-size: 24px;
    font-weight: bold;
    color: #FF4B4B;
    min-height: 35px;
  }
</style>
</head>
<body>
  
  <div id="roulette-container">
    <div class="pointer"></div>
    <canvas id="roulette" width="400" height="400"></canvas>
  </div>
  
  <button id="spinBtn" onclick="spin()">돌리기!</button>
  
  <div id="result"></div>

<script>
  const canvas = document.getElementById("roulette");
  const ctx = canvas.getContext("2d");
  
  // 룰렛 항목들 (원하는 대로 자유롭게 변경하세요!)
  const items = ["꽝", "점심 쏘기", "아이스크림", "커피 쏘기", "간식 쏘기", "다음 기회에"];
  const colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#E8BAFF"];

  const numItems = items.length;
  const anglePerItem = (2 * Math.PI) / numItems;
  const degreesPerItem = 360 / numItems;
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = centerX;

  function drawRoulette() {
    for (let i = 0; i < numItems; i++) {
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, anglePerItem * i - Math.PI / 2, anglePerItem * (i + 1) - Math.PI / 2);
      ctx.fillStyle = colors[i % colors.length];
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#ffffff";
      ctx.stroke();

      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(anglePerItem * i + anglePerItem / 2 - Math.PI / 2);
      ctx.textAlign = "right";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#333";
      ctx.font = "bold 22px '맑은 고딕', sans-serif";
      ctx.fillText(items[i], radius - 20, 0);
      ctx.restore();
    }
  }

  drawRoulette();

  let currentRotation = 0;
  let isSpinning = false;

  function spin() {
    if (isSpinning) return;
    isSpinning = true;
    document.getElementById("spinBtn").disabled = true;
    document.getElementById("result").innerText = "";

    // 100% 랜덤 회전 각도 생성 (기본 5바퀴 + 랜덤 0~360도)
    const randomSpin = Math.random() * 360;
    const spinAngle = (360 * 5) + randomSpin;
    
    currentRotation += spinAngle;
    canvas.style.transform = `rotate(${currentRotation}deg)`;

    // 멈춘 후 바늘이 가리키는 정확한 항목 계산
    const effectiveRotation = currentRotation % 360;
    // 룰렛이 시계방향으로 돌기 때문에, 역산하여 12시 방향(바늘)에 있는 항목을 찾습니다.
    const winningAngle = (360 - effectiveRotation) % 360; 
    const winningIndex = Math.floor(winningAngle / degreesPerItem);
    const resultItem = items[winningIndex];

    setTimeout(() => {
      document.getElementById("result").innerText = `🎉 당첨: ${resultItem} 🎉`;
      isSpinning = false;
      document.getElementById("spinBtn").disabled = false;
      
      // 다음 회전을 위해 각도 초기화 (시각적 변화 없이 내부 수치만 정리)
      currentRotation = currentRotation % 360;
      canvas.style.transition = "none";
      canvas.style.transform = `rotate(${currentRotation}deg)`;
      setTimeout(() => {
         canvas.style.transition = "transform 3.5s cubic-bezier(0.25, 0.1, 0.15, 1)";
      }, 50);
      
    }, 3500);
  }
</script>
</body>
</html>
"""

# Streamlit 화면에 HTML 렌더링
components.html(roulette_html, height=550)