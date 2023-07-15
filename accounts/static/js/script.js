const loginButton = document.getElementById("loginButton");
const signupButton = document.getElementById("signupButton");
const logoutButton = document.getElementById("logoutButton");
const welcomeMessage = document.getElementById("welcomeMessage"); // 추가: 환영 메시지를 표시할 요소

$(document).ready(function() {
  $.ajax({
    url: '/get_session_data/',  // 서버의 API 엔드포인트 경로
    type: 'GET',
    success: function(data) {
      // 세션 데이터 활용
      const username = data.username;
      const isAuthenticated = data.isAuthenticated;

      if (isAuthenticated === 'true') {
        console.log('사용자 인증됨:', username);
        // 인증된 상태에서의 동작 수행
        loginButton.style.display = "none";
        signupButton.style.display = "none";
        logoutButton.style.display = "block";
        welcomeMessage.textContent = username + "님 환영합니다"; // 추가: 환영 메시지 표시
        welcomeMessage.style.display = "block"; // 추가: 환영 메시지 보이기
      } else {
        console.log('사용자 미인증');
        // 비인증 상태에서의 동작 수행
        loginButton.style.display = "block";
        signupButton.style.display = "block";
        logoutButton.style.display = "none";
        welcomeMessage.style.display = "none"; // 추가: 환영 메시지 숨기기
      }
    },
    error: function(error) {
      console.log('세션 데이터 가져오기 실패:', error);
    }
  });
});
