const socket = io("http://127.0.0.1:8000");

const box = document.getElementById("statusBox");
const message = document.getElementById("message");

socket.on("connect", () => {
  console.log("Connected to the server");
});

// when the backend sends data via WebSocket, handle it
socket.on("detection", (data) => {
  console.log("Detection data received:", data);
  const { class_name, user_type } = data;

  // if not a person, reset the status (red)
  if (class_name !== "person") {
    box.style.backgroundColor = "red";
    box.textContent = "Idle";
    message.textContent = "";
    return;
  }

  // If it is a person, process the user type and change the color
  if (user_type === "local") {
    box.style.backgroundColor = "green";
    box.textContent = "Local User";
    message.textContent = "";
  } else if (user_type === "tourist") {
    box.style.backgroundColor = "yellow";
    box.textContent = "Tourist Detected";
    message.textContent = "Please switch lines - it is peak traffic!";
  }

  // keep the color for 3 seconds and then reset it to red
  setTimeout(() => {
    box.style.backgroundColor = "red";
    box.textContent = "Waiting for data...";
    message.textContent = "";
  }, 3000); // in ms
});
