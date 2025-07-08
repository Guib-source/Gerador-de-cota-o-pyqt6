from dataclasses import dataclass

@dataclass
class Onibus:
    origem: str
    destino: str
    data_ida: str
    saida_ida: str
    chegada_ida: str
    data_volta: str = ""
    saida_volta: str = ""
    chegada_volta: str = ""
    somente_ida: bool = False
    valor: str = ""
    
    def gerar_texto(self) -> str:
        texto = (
            f"🚌 Segue sua cotação para a sua próxima viagem:\n\n"
            f"{self.origem} ➡️ {self.destino}\n"
            f"📅 IDA: {self.data_ida}\n"
            f"➡ Saída: {self.saida_ida}h | Chegada: {self.chegada_ida}h\n\n"
        )
        
        if not self.somente_ida:
            texto += (
                f"📅 VOLTA: {self.data_volta}\n"
                f"➡ Saída: {self.saida_volta}h | Chegada: {self.chegada_volta}h\n\n"
            )
        
        texto += (
            f"💰 Valor: R$ {self.valor}\n"
            f"Valores sujeitos à disponibilidade e alteração sem aviso prévio."
            )
        
        return texto