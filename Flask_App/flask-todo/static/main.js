const apiBase = 'http://localhost:8000';

const tasksContainer = document.getElementById('tasksContainer');
const taskCount = document.getElementById('taskCount');
const statusMessage = document.getElementById('statusMessage');
const taskForm = document.getElementById('taskForm');
const taskInput = document.getElementById('taskInput');
const loader = document.getElementById('loader');

// DOM - doc obj model
function setLoading(isLoading) {
    if (!loader) return;
    loader.classList.toggle('visible', isLoading);
}

function showMessage(text, type = 'success') {
    if (!statusMessage) return;
    statusMessage.textContent = text;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.add('visible');
    window.setTimeout(() => {
        statusMessage.classList.remove('visible');
    }, 3200);
}

async function fetchTasks() {
    if (!tasksContainer || !taskCount) return;
    setLoading(true);
    try {
        const response = await fetch(`${apiBase}/todos`);
        if (!response.ok) throw new Error('Unable to load tasks');
        const data = await response.json();
        renderTasks(data.data || []);
    } catch (error) {
        showMessage(error.message, 'error');
        tasksContainer.innerHTML = '<p class="empty-state">Unable to load tasks.</p>';
    } finally {
        setLoading(false);
    }
}

function renderTasks(tasks) {
    taskCount.textContent = tasks.length;
    if (!tasks.length) {
        tasksContainer.innerHTML = '<p class="empty-state">No tasks yet. Add your first task to get started.</p>';
        return;
    }

    tasksContainer.innerHTML = tasks.map(task => {
        return `
            <div class="task-card ${task.completed ? 'completed' : ''}" data-id="${task.id}">
                <div class="task-main">
                    <span class="task-title">${task.title}</span>
                    <span class="task-chip">${task.completed ? 'Completed' : 'Pending'}</span>
                </div>
                <div class="task-actions">
                    <button class="action-btn toggle-btn">${task.completed ? 'Undo' : 'Complete'}</button>
                    <button class="action-btn delete-btn">Delete</button>
                </div>
            </div>
        `;
    }).join('');

    tasksContainer.querySelectorAll('.toggle-btn').forEach(button => {
        button.addEventListener('click', async (event) => {
            const card = event.target.closest('.task-card');
            if (!card) return;
            const id = Number(card.dataset.id);
            const completed = card.classList.contains('completed');
            const title = card.querySelector('.task-title').textContent.trim();
            await toggleTodo(id, !completed, title);
        });
    });

    tasksContainer.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async (event) => {
            const card = event.target.closest('.task-card');
            if (!card) return;
            const id = Number(card.dataset.id);
            card.classList.add('removing');
            await deleteTodo(id);
        });
    });
}

async function toggleTodo(id, completed, title) {
    setLoading(true);
    try {
        const body = { id, title, completed };
        const response = await fetch(`${apiBase}/todos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!response.ok) throw new Error('Unable to update task');
        showMessage('Task updated successfully');
        await fetchTasks();
    } catch (error) {
        showMessage(error.message, 'error');
    } finally {
        setLoading(false);
    }
}

async function deleteTodo(id) {
    try {
        const response = await fetch(`${apiBase}/todos/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Unable to delete task');
        showMessage('Task removed');
        await fetchTasks();
    } catch (error) {
        showMessage(error.message, 'error');
        setLoading(false);
    }
}

async function submitNewTask(event) {
    event.preventDefault();
    if (!taskInput || !taskInput.value.trim()) {
        showMessage('Enter a valid task before submitting', 'error');
        return;
    }

    setLoading(true);
    const title = taskInput.value.trim();
    const newTodo = {
        id: Date.now(),
        title,
        completed: false
    };

    try {
        const response = await fetch(`${apiBase}/todos`, { // fetch - axios
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newTodo)
        });
        if (!response.ok) { //ok - 200
            const error = await response.json();
            throw new Error(error.detail || 'Unable to add task');
        }
        showMessage('Task created!');
        taskInput.value = '';
    } catch (error) {
        showMessage(error.message, 'error');
    } finally {
        setLoading(false);
    }
}

if (tasksContainer) {
    fetchTasks();
}

if (taskForm) {
    taskForm.addEventListener('submit', submitNewTask);
}
