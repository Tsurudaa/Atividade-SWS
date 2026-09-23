let token = null;
let usuarioAtual = null;


async function login() {
    const email = document.getElementById("login-email").value;
    const senha = document.getElementById("login-senha").value;

    const resposta = await fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            senha
        })
    });

    const dados = await resposta.json();

    mostrarResposta(dados);

    if (!resposta.ok) {
        document.getElementById("login-mensagem").textContent =
            dados.detail || "Erro no login.";
        return;
    }

    token = dados.access_token;

    await carregarUsuarioAtual();

    document.getElementById("login-section")
        .classList.add("hidden");

    document.getElementById("app-section")
        .classList.remove("hidden");

    if (usuarioAtual.perfil === "admin") {
        document.getElementById("cadastro-section")
            .classList.remove("hidden");
    } else {
        document.getElementById("cadastro-section")
            .classList.add("hidden");
    }

    if (
        usuarioAtual.perfil === "admin" ||
        usuarioAtual.perfil === "operador"
    ) {
        carregarUsuarios();
    } else {
        carregarMeusDados();
    }
}


async function carregarUsuarioAtual() {
    const resposta = await fetch("/usuarios/me", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    usuarioAtual = await resposta.json();

    document.getElementById("usuario-logado").textContent =
        `${usuarioAtual.nome} - ${usuarioAtual.perfil}`;
}


async function carregarUsuarios() {
    const resposta = await fetch("/usuarios", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const dados = await resposta.json();

    mostrarResposta(dados);

    if (!resposta.ok) {
        return;
    }

    renderizarUsuarios(dados);
}


async function carregarMeusDados() {
    const resposta = await fetch("/usuarios/me", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const dados = await resposta.json();

    mostrarResposta(dados);

    renderizarUsuarios([dados]);
}


function renderizarUsuarios(usuarios) {
    const container = document.getElementById("usuarios");

    container.innerHTML = "";

    usuarios.forEach(usuario => {
        const div = document.createElement("div");

        div.className = "usuario";

        div.innerHTML = `
            <strong>${usuario.nome}</strong><br>
            ${usuario.email}<br>
            Perfil: ${usuario.perfil}<br><br>

            <button onclick="editarUsuario(${usuario.id})">
                Editar
            </button>

            ${
                usuarioAtual.perfil === "admin"
                ? `
                    <button onclick="excluirUsuario(${usuario.id})">
                        Excluir
                    </button>
                `
                : ""
            }
        `;

        container.appendChild(div);
    });
}


async function criarUsuario() {
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    const perfil = document.getElementById("perfil").value;

    const resposta = await fetch("/usuarios", {
        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify({
            nome,
            email,
            senha,
            perfil
        })
    });

    const dados = await resposta.json();

    mostrarResposta(dados);

    if (resposta.ok) {
        carregarUsuarios();
    }
}


async function editarUsuario(id) {
    const respostaUsuario = await fetch(`/usuarios/${id}`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const usuario = await respostaUsuario.json();

    if (!respostaUsuario.ok) {
        mostrarResposta(usuario);
        return;
    }

    const novoNome = prompt(
        "Novo nome:",
        usuario.nome
    );

    if (novoNome === null) {
        return;
    }

    const novoEmail = prompt(
        "Novo e-mail:",
        usuario.email
    );

    if (novoEmail === null) {
        return;
    }

    let novoPerfil = null;

    if (usuarioAtual.perfil === "admin") {
        novoPerfil = prompt(
            "Novo perfil (admin, operador ou cliente):",
            usuario.perfil
        );

        if (novoPerfil === null) {
            return;
        }

        const perfisValidos = [
            "admin",
            "operador",
            "cliente"
        ];

        if (!perfisValidos.includes(novoPerfil)) {
            alert("Perfil inválido.");
            return;
        }
    }

    const resposta = await fetch(`/usuarios/${id}`, {
        method: "PUT",

        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify({
            nome: novoNome,
            email: novoEmail,
            perfil: novoPerfil
        })
    });

    const dados = await resposta.json();

    mostrarResposta(dados);

    if (resposta.ok) {
        if (
            usuarioAtual.perfil === "admin" ||
            usuarioAtual.perfil === "operador"
        ) {
            carregarUsuarios();
        } else {
            carregarMeusDados();
        }
    }
}

async function excluirUsuario(id) {
    const confirmar = confirm(
        "Deseja realmente excluir este usuário?"
    );

    if (!confirmar) {
        return;
    }

    const resposta = await fetch(`/usuarios/${id}`, {
        method: "DELETE",

        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (resposta.status === 204) {
        mostrarResposta({
            mensagem: "Usuário excluído com sucesso."
        });

        carregarUsuarios();
        return;
    }

    const dados = await resposta.json();

    mostrarResposta(dados);
}


function mostrarResposta(dados) {
    document.getElementById("resposta-api").textContent =
        JSON.stringify(dados, null, 2);
}


function logout() {
    token = null;
    usuarioAtual = null;

    document.getElementById("app-section")
        .classList.add("hidden");

    document.getElementById("login-section")
        .classList.remove("hidden");

    document.getElementById("login-email").value = "";
    document.getElementById("login-senha").value = "";
}