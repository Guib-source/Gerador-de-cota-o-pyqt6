from dataclasses import dataclass

@dataclass
class Aereo:
    origem: str
    destino: str
    data_ida: str
    saida_ida: str
    chegada_ida: str
    paradas_ida: str
    data_volta: str = ""
    saida_volta: str = ""
    chegada_volta: str = ""
    paradas_volta: str = ""
    somente_ida: bool = False
    valor: str = ""
    bagagem: str = "Não incluída"

    def gerar_texto(self) -> str:
        texto = (
            f"✈️ Segue sua cotação especial para a sua próxima viagem:\n\n"
            f"{self.origem} ➡️ {self.destino}\n"
            f"📅 IDA: {self.data_ida}\n"
            f"➡ Saída: {self.saida_ida}h | {self.paradas_ida}\n"
            f"➡ Chegada: {self.chegada_ida}h em {self.destino}\n\n"
        )

        if not self.somente_ida:
            texto += (
                f"{self.destino} ➡️ {self.origem}\n"
                f"📅 VOLTA: {self.data_volta}\n"
                f"➡ Saída: {self.saida_volta}h | {self.paradas_volta}\n"
                f"➡ Chegada: {self.chegada_volta}h em {self.origem}\n\n"
                f"💰 Valor: {self.valor} (ida e volta)\n"
                f"🧳 Bagagem: {self.bagagem}\n\n"
                f"Valores sujeitos à disponibilidade e alteração sem aviso prévio."
            )
        else:
            texto += (
                f"💰 Valor: R$ {self.valor} (somente ida)\n"
                f"🧳 Bagagem: {self.bagagem}\n\n"
                f"Valores sujeitos à disponibilidade e alteração sem aviso prévio."
            )

        return texto