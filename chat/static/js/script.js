const loginButton = document.getElementById("loginButton");
const signupButton = document.getElementById("signupButton");
const logoutButton = document.getElementById("logoutButton");
const welcomeMessage = document.getElementById("welcomeMessage");

$(document).ready(function() {
  $.ajax({
    url: '/get_session_data/', 
    type: 'GET',
    success: function(data) {
      const username = data.username;
      const isAuthenticated = data.isAuthenticated;

      if (isAuthenticated === 'true') {
        console.log('사용자 인증됨:', username);
        loginButton.style.display = "none";
        signupButton.style.display = "none";
        logoutButton.style.display = "block";
        welcomeMessage.textContent = username + "님 환영합니다";
        welcomeMessage.style.display = "block"; 
      } else {
        console.log('사용자 미인증');
        loginButton.style.display = "block";
        signupButton.style.display = "block";
        logoutButton.style.display = "none";
        welcomeMessage.style.display = "none";
      }
    },
    error: function(error) {
      console.log('세션 데이터 가져오기 실패:', error);
    }
  });

  
});

$("#community").on("click", function() {
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
    }
  });
});