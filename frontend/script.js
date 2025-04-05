const socket = io();
const box = document.getElementById("statusBox");
const message = document.getElementById("message");

socket.on("detection", (data) => {
  const { class_name, user_type } = data;

  if (class_name !== "person") {
    box.style.backgroundColor = "red";
    box.textContent = "Idle";
    message.textContent = "";
    return;
  }

  if (user_type === "local") {
    box.style.backgroundColor = "green";
    box.textContent = "Local User";
    message.textContent = "";
  } else if (user_type === "tourist") {
    box.style.backgroundColor = "yellow";
    box.textContent = "Tourist Detected";
    message.textContent = "Please switch lines - it is peak traffic!";
  }
});
