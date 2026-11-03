// AproveitaJá - comportamentos do front-end

document.addEventListener("DOMContentLoaded", () => {
  // Correção BUG-04: desabilita o botão após o primeiro clique para evitar envio duplicado
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", (evento) => {
      // Melhoria SUG-03: confirmação antes de excluir
      const mensagem = form.dataset.confirmar;
      if (mensagem && !window.confirm(mensagem)) {
        evento.preventDefault();
        return;
      }
      if (form.method.toLowerCase() === "post") {
        form.querySelectorAll("button[type=submit]").forEach((botao) => {
          botao.disabled = true;
          botao.dataset.textoOriginal = botao.textContent;
          botao.textContent = "Salvando…";
        });
      }
    });
  });

  // Menu recolhível no celular
  const botaoMenu = document.querySelector("[data-menu]");
  const menu = document.getElementById("menu");
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", () => menu.classList.toggle("aberto"));
  }

  // Alertas somem sozinhos após 6 segundos
  document.querySelectorAll(".alerta-sucesso").forEach((alerta) => {
    setTimeout(() => alerta.remove(), 6000);
  });
});
