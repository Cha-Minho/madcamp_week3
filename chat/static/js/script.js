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

$("#community").on("click", function() {
  // 새로운 채팅방 생성 또는 기존 채팅방 입장 선택 다이얼로그 표시
  Swal.fire({
    title: "커뮤니티 입장",
    text: "원하시는 버튼을 클릭하세요.",
    icon: "question",
    showCloseButton: true,
    showCancelButton: true,
    confirmButtonText: "새로운 채팅방 생성",
    cancelButtonText: "기존 채팅방 입장",
    allowOutsideClick: true,
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "채팅방 만들기",
        input: "text",
        inputPlaceholder: "채팅방 이름(한글 입력 불가능)",
        showCloseButton: true,
        showCancelButton: true,
        confirmButtonText: "생성하기",
        cancelButtonText: "취소",
        allowOutsideClick: true,
        preConfirm: (roomName) => {
          if (!roomName) {
            Swal.showValidationMessage("채팅방 이름을 입력해주세요");
          } else {
            var form = document.createElement('form');
            form.method = 'POST';
            form.action = '/chat/' + roomName + '/';
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrfmiddlewaretoken';
            input.value = '{{ csrf_token }}';
            form.appendChild(input);
            var roomNameInput = document.createElement('input');
            roomNameInput.type = 'hidden';
            roomNameInput.name = 'room_name';
            roomNameInput.value = roomName;
            form.appendChild(roomNameInput);
            document.body.appendChild(form);
            form.submit();
          }
        },
      });
    } else if (result.dismiss === Swal.DismissReason.cancel) {
      window.location.href = "/chat_list/";
    } else {
      // 기존 채팅방 리스트 페이지로 이동 (페이지 주소에 따라 변경)
    }
  });
});