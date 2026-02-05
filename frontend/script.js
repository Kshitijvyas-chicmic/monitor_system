const API_BASE = "http://localhost:8000";
let token = localStorage.getItem("token");
let currentUser = null;

// Safely parse user from localStorage
try {
  const userData = localStorage.getItem("user");
  currentUser = userData ? JSON.parse(userData) : null;
} catch (error) {
  console.error("Error parsing user data from localStorage:", error);
  localStorage.removeItem("user");
  localStorage.removeItem("token");
  token = null;
}
// console.log("Token being used:", token);

if (token && currentUser) {
  showAppSection();
} else {
  showLogin();
}

// async function register() {
//   event.preventDefault();
//   const email = document.getElementById("reg-email").value;
//   const name = document.getElementById("reg-name").value;
//   const password = document.getElementById("reg-password").value;
//   const role = document.getElementById("reg-role").value;

//   const response = await fetch(`${API_BASE}/auth/signup`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ email, name, password, role }),
//   });
//   const data = await response.json();
//   alert(response.ok ? "Registered successfully!" : `Error: ${data.detail}`);
// }
// async function register() {
//   event.preventDefault();
//   const email = document.getElementById("reg-email").value;
//   const name = document.getElementById("reg-name").value;
//   const password = document.getElementById("reg-password").value;
//   const role = document.getElementById("reg-role").value;

//   const response = await fetch(`${API_BASE}/auth/signup`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ email, name, password, role }),
//   });
//   const data = await response.json();

//   if (response.ok) {
//     alert("Registered successfully! Please verify your email.");
//     // Hide login & register cards
//     document.getElementById("login-card").style.display = "none";
//     document.getElementById("register-card").style.display = "none";

//     // Show verification section
//     document.getElementById("verify-email-section").style.display = "block";

//     // Pre-fill email in verification form
//     document.getElementById("verify-email-input").value = email;
//   } else {
//     alert(`Error: ${data.detail}`);
//   }
// }

// async function verifyEmail() {
//   const email = document.getElementById("verify-email-input").value;
//   const token = document.getElementById("verify-token-input").value;

//   if (!email || !token) {
//     alert("Please provide both email and token.");
//     return;
//   }

//   try {
//     const response = await fetch(`${API_BASE}/auth/verify-email`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ email: email, token: token }),
//     });

//     const data = await response.json();

//     if (response.ok) {
//       alert("Email verified successfully!");
//       // Hide verification form after success
//       document.getElementById("verify-email-section").style.display = "none";
//       // Show main app section
//       document.getElementById("app-section").style.display = "block";
//     } else {
//       alert(`Verification failed: ${data.detail}`);
//     }
//   } catch (err) {
//     console.error("Error verifying email:", err);
//     alert("Something went wrong. Please try again.");
//   }
// }

// async function login() {
//   event.preventDefault();
//   const email = document.getElementById("login-email").value;
//   const password = document.getElementById("login-password").value;

//   try {
//     const response = await fetch(`${API_BASE}/auth/login`, {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ email, password }),
//     });
//     const data = await response.json();

//     if (response.ok && data.user) {
//       token = data.access_token;
//       currentUser = data.user;
//       localStorage.setItem("token", token);
//       localStorage.setItem("user", JSON.stringify(currentUser));
//       showAppSection();
//     } else {
//       alert(`Login failed: ${data.detail || "Unknown error"}`);
//     }
//   } catch (error) {
//     console.error("Login error:", error);
//     alert("Network error. Please try again.");
//   }
// }

// async function register() {
//   event.preventDefault();
//   const email = document.getElementById("reg-email").value;
//   const name = document.getElementById("reg-name").value;
//   const password = document.getElementById("reg-password").value;
//   const role = document.getElementById("reg-role").value;

//   try {
//     const response = await fetch(`${API_BASE}/auth/signup`, {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ email, name, password, role }),
//     });

//     const data = await response.json();
//     // signup success
//     navigate("/verify-email", {
//       state: { email: response.email },
//     });

//     if (response.ok) {
//       alert(
//         "Registered successfully! Check your email for verification token.",
//       );

//       // Show the email verification form
//       document.getElementById("register-card").style.display = "none";
//       document.getElementById("verify-email-section").style.display = "block";

//       // Pre-fill the email field for verification
//       document.getElementById("verify-email-input").value = email;
//     } else {
//       alert(`Error: ${data.detail}`);
//     }
//   } catch (err) {
//     console.error("Registration error:", err);
//     alert("Network error. Please try again.");
//   }
// }

async function register() {
  event.preventDefault();

  const email = document.getElementById("reg-email").value;
  const name = document.getElementById("reg-name").value;
  const password = document.getElementById("reg-password").value;
  const role = document.getElementById("reg-role").value;

  try {
    const response = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, name, password, role }),
    });

    const data = await response.json();

    if (response.ok) {
      alert(
        "Registered successfully! Check your email for verification token.",
      );

      // 👇 LOGIN & REGISTER HIDE
      document.getElementById("login-card").style.display = "none";
      document.getElementById("register-card").style.display = "none";

      // 👇 VERIFY SECTION SHOW
      document.getElementById("verify-email-section").style.display = "block";

      // 👇 EMAIL AUTO-FILL
      document.getElementById("verify-email-input").value = email;
    } else {
      alert(`Error: ${data.detail}`);
    }
    verifyEmail();
  } catch (err) {
    console.error("Registration error:", err);
    alert("Network error. Please try again.");
  }
}

async function login() {
  event.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok && data.user) {
      // Check if user is verified
      if (!data.user.is_verified) {
        alert(
          "Your email is not verified yet. Please verify your email first.",
        );

        // Show the verification form
        document.getElementById("login-card").style.display = "none";
        document.getElementById("verify-email-section").style.display = "block";

        // Pre-fill email
        document.getElementById("verify-email-input").value = email;
        return;
      }

      token = data.access_token;
      currentUser = data.user;
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(currentUser));
      showAppSection();
    } else {
      alert(`Login failed: ${data.detail || "Unknown error"}`);
    }
  } catch (error) {
    console.error("Login error:", error);
    alert("Network error. Please try again.");
  }
}

// Initialize Google Auth on load
// window.onload = function () {
//   initializeGoogleAuth();
// };

async function initializeGoogleAuth() {
  try {
    const response = await fetch(`${API_BASE}/auth/google-client-id`);
    const data = await response.json();
    console.log(data.client_id);
    if (data.client_id) {
      google.accounts.id.initialize({
        client_id: data.client_id,
        callback: handleGoogleCredentialResponse,
      });
      google.accounts.id.renderButton(
        document.getElementById("google-btn-container"),
        { theme: "outline", size: "large", width: "100%" },
      );
    }
  } catch (error) {
    console.error("Failed to initialize Google Auth:", error);
  }
}

async function handleGoogleCredentialResponse(response) {
  console.log("Google ID Token received:", response.credential);
  try {
    const res = await fetch(`${API_BASE}/auth/oauth/google`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_token: response.credential }),
    });

    const data = await res.json();

    if (res.ok && data.user) {
      token = data.access_token;
      currentUser = data.user;
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(currentUser));
      showAppSection();
    } else {
      alert(`Google Login failed: ${data.detail || "Unknown error"}`);
    }
  } catch (error) {
    console.error("Google Login Error", error);
    alert("Network error during Google Login.");
  }
}

async function loginWithGithub() {
  try {
    const res = await fetch(`${API_BASE}/auth/github-client-id`);
    const data = await res.json();

    if (!data.client_id) {
      alert("GitHub Client ID not found");
      return;
    }

    const githubAuthUrl =
      `https://github.com/login/oauth/authorize` +
      `?client_id=${data.client_id}` +
      `&redirect_uri=${encodeURIComponent(
        "http://127.0.0.1:5500/frontend/index.html",
      )}` +
      `&scope=user:email`;

    window.location.href = githubAuthUrl;
  } catch (error) {
    console.error("GitHub login error", error);
  }
}
let githubHandled = false;

async function handleGithubCallbackIfPresent() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get("code");

  if (!code) return;

  try {
    const res = await fetch(`${API_BASE}/auth/oauth/github`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });

    const data = await res.json();
    console.log("GitHub login response:", data); // 🔥 debug

    if (!res.ok || !data.access_token || !data.user) {
      alert("GitHub login failed");
      return;
    }

    // ✅ SAME AS GOOGLE
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));

    // ✅ REMOVE ?code= from URL
    window.history.replaceState({}, document.title, window.location.pathname);

    // 🔥 THIS LINE WAS MISSING / NOT RUNNING
    setTimeout(() => {
      showAppSection();
    }, 0);
  } catch (err) {
    console.error("GitHub login error", err);
  }
}

async function verifyEmail() {
  const email = document.getElementById("verify-email-input").value;
  const tokenInput = document.getElementById("verify-token-input").value;

  if (!email || !tokenInput) {
    alert("Please provide both email and token.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/auth/verify-email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, token: tokenInput }),
    });

    const data = await response.json();

    if (!response.ok) {
      alert(`Verification failed: ${data.detail}`);
      return;
    }

    // ✅ SAVE TOKEN + USER
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));

    token = data.access_token;
    currentUser = data.user;

    // ✅ HIDE VERIFY SECTION
    document.getElementById("verify-email-section").style.display = "none";

    // ✅ OPEN DASHBOARD DIRECTLY
    showLogin();
  } catch (err) {
    console.error("Verify email error:", err);
    alert("Something went wrong");
  }
}

// Auth flow functions
function showLogin() {
  document.getElementById("login-card").style.display = "block";
  document.getElementById("register-card").style.display = "none";
  document.querySelector(".auth-section").style.display = "grid";
  document.getElementById("app-section").style.display = "none";
}

function showRegister() {
  document.getElementById("login-card").style.display = "none";
  document.getElementById("register-card").style.display = "block";
  document.querySelector(".auth-section").style.display = "grid";
  document.getElementById("app-section").style.display = "none";
}

function logout() {
  token = null;
  currentUser = null;
  localStorage.clear();
  showLogin();
}

function showAppSection() {
  // Add null check for currentUser
  if (!currentUser) {
    console.error("No user data available");
    showLogin();
    return;
  }

  document.querySelector(".auth-section").style.display = "none";
  document.getElementById("app-section").style.display = "block";

  // Add null checks for DOM elements
  const userNameElement = document.getElementById("user-name");
  const userRoleElement = document.getElementById("user-role");

  if (userNameElement) {
    userNameElement.textContent = currentUser.name || "User";
  }
  if (userRoleElement) {
    userRoleElement.textContent = currentUser.role || "Unknown";
  }

  // Add null checks for role-based sections
  if (currentUser.role === "admin") {
    const userManagement = document.getElementById("user-management");
    const adminTaskSection = document.getElementById("admin-task-section");
    const activitiesSection = document.getElementById("activities-section");
    const reportsSection = document.getElementById("reports-section");

    if (userManagement) userManagement.style.display = "block";
    if (adminTaskSection) adminTaskSection.style.display = "block";
    if (activitiesSection) activitiesSection.style.display = "block";
    if (reportsSection) reportsSection.style.display = "block";
  } else if (currentUser.role === "manager") {
    const adminTaskSection = document.getElementById("admin-task-section");
    if (adminTaskSection) adminTaskSection.style.display = "block";
  }
}

// User Management Functions
async function listUsers() {
  const response = await fetch(`${API_BASE}/auth/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const users = await response.json();
  if (response.ok) {
    const list = document.getElementById("users-list");
    list.innerHTML = "";
    users.forEach((user) => {
      const li = document.createElement("li");
      li.textContent = `${user.id}: ${user.name} (${user.email}) - ${user.role}`;
      list.appendChild(li);
    });
  } else {
    alert(`Error: ${users.detail}`);
  }
}

async function getUserById() {
  const userId = document.getElementById("get-user-id").value;
  const response = await fetch(`${API_BASE}/auth/user_id/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const user = await response.json();
  if (response.ok) {
    document.getElementById("user-details").innerHTML = JSON.stringify(
      user,
      null,
      2,
    );
  } else {
    alert(`Error: ${user.detail}`);
  }
}

async function updateUser() {
  const userId = document.getElementById("update-user-id").value;
  const name = document.getElementById("update-name").value;
  const email = document.getElementById("update-email").value;
  const response = await fetch(`${API_BASE}/auth/user_id/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name, email }),
  });
  const data = await response.json();
  alert(response.ok ? "User updated!" : `Error: ${data.detail}`);
}

async function deleteUser() {
  const userId = document.getElementById("delete-user-id").value;
  if (!userId) {
    alert("Please enter a User ID");
    return;
  }

  if (
    !confirm(
      `Are you sure you want to delete user ${userId}? This action cannot be undone.`,
    )
  ) {
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/auth/user_id/${userId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.ok) {
      alert("User deleted successfully!");
      // Optionally refresh the user list
      listUsers();
    } else {
      const data = await response.json();
      alert(`Error deleting user: ${data.detail || "Unknown error"}`);
    }
  } catch (error) {
    alert(`Network error: ${error.message}`);
  }
}

async function changePassword() {
  const userId = document.getElementById("change-pwd-user-id").value;
  const oldPassword = document.getElementById("old-password").value;
  const newPassword = document.getElementById("new-password").value;
  const response = await fetch(`${API_BASE}/auth/change-password/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      old_password: oldPassword,
      new_password: newPassword,
    }),
  });
  const data = await response.json();
  alert(response.ok ? "Password changed!" : `Error: ${data.detail}`);
}

async function changeRole() {
  const userId = document.getElementById("role-user-id").value;
  const role = document.getElementById("new-role").value;
  const response = await fetch(`${API_BASE}/auth/${userId}/role`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ role }),
  });
  const data = await response.json();
  alert(response.ok ? "Role changed!" : `Error: ${data.detail}`);
}

// Task Management Functions
async function createTask() {
  const title = document.getElementById("task-title").value;
  const description = document.getElementById("task-description").value;
  const priority = document.getElementById("task-priority").value;
  const status = document.getElementById("task-status").value;
  const assigned_to_email = document.getElementById("task-assignee").value;
  const due_date = document.getElementById("task-due-date").value;

  const response = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title,
      description,
      priority,
      status,
      assigned_to_email,
      due_date: due_date || null,
    }),
  });
  const data = await response.json();
  alert(response.ok ? "Task created!" : `Error: ${data.detail}`);
}

async function fetchMyTasks() {
  const response = await fetch(`${API_BASE}/tasks/my`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const tasks = await response.json();
  if (response.ok) {
    const list = document.getElementById("my-tasks");
    list.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.textContent = `${task.id}: ${task.title} - ${task.description} (${task.priority}, ${task.status})`;
      list.appendChild(li);
    });
  } else {
    alert(`Error: ${tasks.detail}`);
  }
}

async function fetchAllTasks() {
  const response = await fetch(`${API_BASE}/tasks/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const tasks = await response.json();
  if (response.ok) {
    const list = document.getElementById("all-tasks");
    list.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.textContent = `${task.id}: ${task.title} - ${task.description} (${task.priority}, ${task.status})`;
      list.appendChild(li);
    });
  } else {
    alert(`Error: ${tasks.detail}`);
  }
}

async function getTaskById() {
  const taskId = document.getElementById("get-task-id").value;
  const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const task = await response.json();
  if (response.ok) {
    document.getElementById("task-details").innerHTML = JSON.stringify(
      task,
      null,
      2,
    );
  } else {
    alert(`Error: ${task.detail}`);
  }
}

async function updateTask() {
  const taskId = document.getElementById("update-task-id").value;
  const title = document.getElementById("update-task-title").value;
  const description = document.getElementById("update-task-description").value;
  const priority = document.getElementById("update-task-priority").value;
  const due_date = document.getElementById("update-task-due-date").value;

  const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title,
      description,
      priority,
      due_date: due_date || null,
    }),
  });
  const data = await response.json();
  alert(response.ok ? "Task updated!" : `Error: ${data.detail}`);
}

async function updateTaskStatus() {
  const taskId = document.getElementById("status-task-id").value;
  const status = document.getElementById("new-status").value;
  const response = await fetch(`${API_BASE}/tasks/${taskId}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ status }),
  });
  const data = await response.json();
  alert(response.ok ? "Status updated!" : `Error: ${data.detail}`);
}

async function reassignTask() {
  const taskId = document.getElementById("reassign-task-id").value;
  const newUserId = document.getElementById("new-assignee-id").value;
  const response = await fetch(
    `${API_BASE}/tasks/${taskId}/assign?new_user_id=${newUserId}`,
    {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token}` },
    },
  );
  const data = await response.json();
  alert(response.ok ? "Task reassigned!" : `Error: ${data.detail}`);
}

async function deleteTask() {
  const taskId = document.getElementById("delete-task-id").value;
  const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await response.json();
  alert(response.ok ? "Task deleted!" : `Error: ${data.detail}`);
}

async function filterTasks() {
  const status = document.getElementById("filter-status").value;
  const priority = document.getElementById("filter-priority").value;
  const assigned_to_id = document.getElementById("filter-assigned-to").value;
  const sort_by = document.getElementById("sort-by").value;
  const order = document.getElementById("order").value;
  const page = document.getElementById("page").value;
  const page_size = document.getElementById("page-size").value;

  const params = new URLSearchParams();
  if (status) params.append("status", status);
  if (priority) params.append("priority", priority);
  if (assigned_to_id) params.append("assigned_to_id", assigned_to_id);
  params.append("sort_by", sort_by);
  params.append("order", order);
  params.append("page", page);
  params.append("page_size", page_size);

  const response = await fetch(`${API_BASE}/tasks/filter?${params}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await response.json();
  if (response.ok) {
    const container = document.getElementById("filtered-tasks");
    container.innerHTML = `<h4>Filtered Tasks (Page ${data.page} of ${data.total_pages}, Total: ${data.total})</h4>`;
    const list = document.createElement("ul");
    data.tasks.forEach((task) => {
      const li = document.createElement("li");
      li.textContent = `${task.id}: ${task.title} - ${task.description} (${task.priority}, ${task.status})`;
      list.appendChild(li);
    });
    container.appendChild(list);
  } else {
    alert(`Error: ${data.detail}`);
  }
}

// Comments Functions
async function addComment() {
  const taskId = document.getElementById("comment-task-id").value;
  const content = document.getElementById("comment-content").value;
  const response = await fetch(`${API_BASE}/tasks/${taskId}/comments`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ content }),
  });
  const data = await response.json();
  alert(response.ok ? "Comment added!" : `Error: ${data.detail}`);
}

async function listComments() {
  const taskId = document.getElementById("comment-task-id").value;
  const response = await fetch(`${API_BASE}/tasks/${taskId}/comments`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const comments = await response.json();
  if (response.ok) {
    const list = document.getElementById("comments-list");
    list.innerHTML = "";
    comments.forEach((comment) => {
      const li = document.createElement("li");
      li.textContent = `${comment.id}: ${comment.content} by ${comment.user_name}`;
      list.appendChild(li);
    });
  } else {
    alert(`Error: ${comments.detail}`);
  }
}

async function updateComment() {
  const taskId = document.getElementById("update-comment-task-id").value;
  const commentId = document.getElementById("update-comment-id").value;
  const content = document.getElementById("update-comment-content").value;

  console.log("Updating comment:", { taskId, commentId, content });

  const response = await fetch(
    `${API_BASE}/tasks/${taskId}/comments/${commentId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content }),
    },
  );

  const data = await response.json();
  alert(response.ok ? "Comment updated!" : `Error: ${data.detail}`);
}

async function deleteComment() {
  const taskId = document.getElementById("delete-comment-task-id").value;
  const commentId = document.getElementById("delete-comment-id").value;

  console.log("Deleting comment:", { taskId, commentId });

  const response = await fetch(
    `${API_BASE}/tasks/${taskId}/comments/${commentId}`,
    {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    },
  );

  const data = await response.json();
  alert(response.ok ? "Comment deleted!" : `Error: ${data.detail}`);
}

// Roles Functions
// Activities Functions
async function listAllActivities() {
  const response = await fetch(`${API_BASE}/activities`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const activities = await response.json();
  if (response.ok) {
    const list = document.getElementById("all-activities");
    list.innerHTML = "";
    activities.forEach((activity) => {
      const li = document.createElement("li");
      li.textContent = `${activity.id}: ${activity.action} on ${activity.entity_type} ${activity.entity_id} by ${activity.user_name}`;
      list.appendChild(li);
    });
  } else {
    alert(`Error: ${activities.detail}`);
  }
}

async function getTaskActivities() {
  const taskId = document.getElementById("activity-task-id").value;
  const response = await fetch(`${API_BASE}/activities/task/${taskId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const activities = await response.json();
  if (response.ok) {
    const list = document.getElementById("task-activities");
    list.innerHTML = "";
    activities.forEach((activity) => {
      const li = document.createElement("li");
      li.textContent = `${activity.id}: ${activity.action} by ${activity.user_name}`;
      list.appendChild(li);
    });
  } else {
    alert(`Error: ${activities.detail}`);
  }
}

async function getUserActivities() {
  const userId = document.getElementById("activity-user-id").value;
  console.log("Fetching activities for user:", userId);
  const response = await fetch(`${API_BASE}/activities/user/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const activities = await response.json();
  console.log("Response status:", response.status);
  console.log("Activities data:", activities);
  if (response.ok) {
    const list = document.getElementById("user-activities");
    list.innerHTML = "";
    activities.forEach((activity) => {
      const li = document.createElement("li");
      li.textContent = `${activity.id}: ${activity.action} on ${activity.entity_type} ${activity.entity_id} by ${activity.user_name}`;
      list.appendChild(li);
    });
    console.log("Activities displayed:", activities.length);
  } else {
    alert(`Error: ${activities.detail}`);
    console.error("Error fetching user activities:", activities);
  }
}

// PDF Report Download Function
async function downloadReportPDF(event) {
  // Prevent default action if called from a form or link
  if (event) event.preventDefault();

  const statusElement = document.getElementById("report-status");
  const token = localStorage.getItem("token"); // match the key exactly
  console.log("Token being used:", token);
  try {
    // Show loading status
    statusElement.style.display = "block";
    statusElement.className = "status-message info";
    statusElement.textContent = "Generating PDF report...";

    const response = await fetch(`${API_BASE}/reports/pdf`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.ok) {
      // Get the blob from the response
      const blob = await response.blob();

      // Create a temporary URL for the blob
      const url = window.URL.createObjectURL(blob);

      // Create a temporary anchor element and trigger download
      const a = document.createElement("a");
      a.href = url;
      a.download = "task_report.pdf";
      document.body.appendChild(a);
      a.click();

      // Delay cleanup to ensure download starts
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }, 100);

      // Show success message
      statusElement.className = "status-message success";
      statusElement.textContent = "PDF report downloaded successfully!";

      // Hide status after 3 seconds
      setTimeout(() => {
        statusElement.style.display = "none";
      }, 3000);
    } else {
      // Handle server errors
      const errorData = await response
        .json()
        .catch(() => ({ detail: "Unknown error" }));
      statusElement.className = "status-message error";
      statusElement.textContent = `Failed to download PDF: ${errorData.detail}`;

      console.error("PDF download failed:", errorData);
    }
  } catch (error) {
    console.error("Network error during PDF download:", error);
    statusElement.className = "status-message error";
    statusElement.textContent = "Network error: Unable to download PDF report";
  }
}
document.addEventListener("DOMContentLoaded", () => {
  initializeGoogleAuth();
  handleGithubCallbackIfPresent();
});
