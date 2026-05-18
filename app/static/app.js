const form = document.querySelector("#player-form");
const playerIdInput = document.querySelector("#player-id");
const nameInput = document.querySelector("#name");
const positionInput = document.querySelector("#position");
const numberInput = document.querySelector("#number");
const submitButton = document.querySelector("#submit-button");
const resetButton = document.querySelector("#reset-button");
const refreshButton = document.querySelector("#refresh-button");
const tableBody = document.querySelector("#players-table");
const emptyState = document.querySelector("#empty-state");
const playerCount = document.querySelector("#player-count");
const statusBox = document.querySelector("#status");

let players = [];

function setStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", isError);
}

function getPayload() {
  return {
    name: nameInput.value.trim(),
    position: positionInput.value,
    number: Number(numberInput.value),
  };
}

function resetForm() {
  playerIdInput.value = "";
  form.reset();
  positionInput.value = "Levantador";
  submitButton.textContent = "Salvar";
}

function renderPlayers() {
  tableBody.innerHTML = "";
  emptyState.classList.toggle("visible", players.length === 0);
  playerCount.textContent = `${players.length} jogador${players.length === 1 ? "" : "es"}`;

  for (const player of players) {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${player.id}</td>
      <td>${player.name}</td>
      <td>${player.position}</td>
      <td>${player.number}</td>
      <td>
        <div class="actions">
          <button class="action edit" type="button" data-action="edit" data-id="${player.id}">Editar</button>
          <button class="action delete" type="button" data-action="delete" data-id="${player.id}">Remover</button>
        </div>
      </td>
    `;

    tableBody.appendChild(row);
  }
}

async function loadPlayers() {
  try {
    setStatus("Atualizando");
    const response = await fetch("/players");

    if (!response.ok) {
      throw new Error("Nao foi possivel carregar jogadores");
    }

    players = await response.json();
    renderPlayers();
    setStatus("Online");
  } catch (error) {
    setStatus(error.message, true);
  }
}

async function savePlayer(event) {
  event.preventDefault();

  const playerId = playerIdInput.value;
  const isEditing = playerId !== "";
  const url = isEditing ? `/players/${playerId}` : "/players";
  const method = isEditing ? "PUT" : "POST";

  try {
    setStatus("Salvando");
    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(getPayload()),
    });

    if (!response.ok) {
      throw new Error("Dados invalidos");
    }

    resetForm();
    await loadPlayers();
  } catch (error) {
    setStatus(error.message, true);
  }
}

async function deletePlayer(playerId) {
  try {
    setStatus("Removendo");
    const response = await fetch(`/players/${playerId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Nao foi possivel remover");
    }

    await loadPlayers();
  } catch (error) {
    setStatus(error.message, true);
  }
}

function editPlayer(playerId) {
  const player = players.find((item) => item.id === Number(playerId));
  if (!player) {
    return;
  }

  playerIdInput.value = player.id;
  nameInput.value = player.name;
  positionInput.value = player.position;
  numberInput.value = player.number;
  submitButton.textContent = "Atualizar";
  nameInput.focus();
}

tableBody.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) {
    return;
  }

  const { action, id } = button.dataset;

  if (action === "edit") {
    editPlayer(id);
  }

  if (action === "delete") {
    deletePlayer(id);
  }
});

form.addEventListener("submit", savePlayer);
resetButton.addEventListener("click", resetForm);
refreshButton.addEventListener("click", loadPlayers);

loadPlayers();
