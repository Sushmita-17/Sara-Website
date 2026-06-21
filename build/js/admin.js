// Admin Dashboard Logic
document.addEventListener('DOMContentLoaded', function() {
    const user = getUser();
    const token = getToken();

    // Protection: Redirect if not admin/staff
    if (!user || (user.role !== 'admin' && user.role !== 'staff')) {
        window.location.href = '/login.html?next=admin.html';
        return;
    }

    document.getElementById('admin-name').textContent = user.name;
    
    // View toggling
    const views = {
        'dashboard': document.getElementById('view-dashboard'),
        'users': document.getElementById('view-users'),
        'products': document.getElementById('view-products')
    };
    const title = document.getElementById('page-title');
    const sub = document.getElementById('page-sub');

    function showView(viewName) {
        Object.keys(views).forEach(k => {
            views[k].style.display = k === viewName ? 'block' : 'none';
        });
        
        document.querySelectorAll('.admin-nav a').forEach(a => a.classList.remove('active'));
        document.getElementById('btn-' + viewName).classList.add('active');

        if (viewName === 'dashboard') {
            title.textContent = 'Dashboard Overview';
            sub.textContent = 'Key performance indicators';
            loadStats();
        } else if (viewName === 'users') {
            title.textContent = 'User Management';
            sub.textContent = 'View and manage platform members';
            loadUsers();
        } else if (viewName === 'products') {
            title.textContent = 'Inventory Management';
            sub.textContent = 'Manage your product catalog';
        }
    }

    document.getElementById('btn-dashboard').onclick = () => showView('dashboard');
    document.getElementById('btn-users').onclick = () => showView('users');
    document.getElementById('btn-products').onclick = () => showView('products');

    // Initial load
    showView('dashboard');

    function loadStats() {
        fetch(API + '/admin/stats', {
            headers: { 'Authorization': 'Bearer ' + token }
        })
        .then(r => r.json())
        .then(data => {
            document.getElementById('stat-users').textContent = data.total_users;
            document.getElementById('stat-products').textContent = data.total_products;
            document.getElementById('stat-admins').textContent = data.roles.admin || 0;
            document.getElementById('stat-staff').textContent = data.roles.staff || 0;
        })
        .catch(err => console.error('Stats Error:', err));
    }

    function loadUsers() {
        const tableBody = document.getElementById('user-table-body');
        tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Loading users...</td></tr>';

        fetch(API + '/admin/users', {
            headers: { 'Authorization': 'Bearer ' + token }
        })
        .then(r => r.json())
        .then(users => {
            tableBody.innerHTML = users.map(u => `
                <tr>
                    <td style="font-weight:700; color:var(--brand-primary);">${u.full_name}</td>
                    <td>${u.email}</td>
                    <td><span class="badge badge-${u.role}">${u.role}</span></td>
                    <td>${u.is_verified ? '✅' : '❌'}</td>
                    <td>${new Date(u.created_at).toLocaleDateString()}</td>
                    <td>
                        <select onchange="updateRole(${u.id}, this.value)" style="padding:6px; border-radius:8px; border:1px solid var(--border);">
                            <option value="customer" ${u.role === 'customer' ? 'selected' : ''}>Customer</option>
                            <option value="staff" ${u.role === 'staff' ? 'selected' : ''}>Staff</option>
                            <option value="admin" ${u.role === 'admin' ? 'selected' : ''}>Admin</option>
                        </select>
                    </td>
                </tr>
            `).join('');
        })
        .catch(err => {
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:red;">Error loading users.</td></tr>';
        });
    }

    window.updateRole = function(userId, newRole) {
        if (!confirm('Are you sure you want to change this user\'s role to ' + newRole + '?')) return;

        fetch(API + '/admin/users/' + userId + '/role', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token 
            },
            body: JSON.stringify({ role: newRole })
        })
        .then(r => r.json())
        .then(data => {
            alert(data.message);
            loadUsers();
        })
        .catch(err => alert('Failed to update role.'));
    };
});
