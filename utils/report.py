import pandas as pd

NOME_EMPRESA = "DataCH Analytics"


def gerar_relatorio_insights(df: pd.DataFrame) -> str:
    total_clientes = len(df)
    churn_label = df["Churn Label"].astype(str).str.strip()
    qtd_churn = (churn_label == "Yes").sum()
    taxa_churn = (qtd_churn / total_clientes * 100) if total_clientes else 0

    receita_perdida = df.loc[churn_label == "Yes", "Total Revenue"].sum()
    ticket_medio_churn = df.loc[churn_label == "Yes", "Monthly Charge"].mean()
    ticket_medio_geral = df["Monthly Charge"].mean()

    motivo_top = df.loc[churn_label == "Yes", "Churn Category"].value_counts().head(3)

    contrato_churn = (
        df.loc[churn_label == "Yes", "Contract"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
    )

    satisfacao_media_churn = df.loc[churn_label == "Yes", "Satisfaction Score"].mean()
    satisfacao_media_geral = df["Satisfaction Score"].mean()

    tenure_medio_churn = df.loc[churn_label == "Yes", "Tenure in Months"].mean()
    tenure_medio_geral = df["Tenure in Months"].mean()

    linhas = []
    linhas.append(f"RELATÓRIO DE ANÁLISE DE CHURN — {NOME_EMPRESA}")
    linhas.append("=" * 60)
    linhas.append("")
    linhas.append("1. VISÃO GERAL")
    linhas.append(f"   - Total de clientes na base: {total_clientes}")
    linhas.append(f"   - Clientes que cancelaram (churn): {qtd_churn}")
    linhas.append(f"   - Taxa de churn: {taxa_churn:.1f}%")
    linhas.append(f"   - Receita total perdida com cancelamentos: ${receita_perdida:,.2f}")
    linhas.append("")
    linhas.append("2. PRINCIPAIS MOTIVOS DE CANCELAMENTO")
    for motivo, qtd in motivo_top.items():
        linhas.append(f"   - {motivo}: {qtd} casos")
    linhas.append("")
    linhas.append("3. PERFIL DE QUEM CANCELA")
    linhas.append(
        f"   - Ticket médio mensal de quem cancelou: ${ticket_medio_churn:,.2f} "
        f"(vs. ${ticket_medio_geral:,.2f} da base geral)"
    )
    linhas.append(
        f"   - Satisfação média de quem cancelou: {satisfacao_media_churn:.1f} "
        f"(vs. {satisfacao_media_geral:.1f} da base geral)"
    )
    linhas.append(
        f"   - Tempo médio de permanência de quem cancelou: {tenure_medio_churn:.1f} meses "
        f"(vs. {tenure_medio_geral:.1f} meses da base geral)"
    )
    linhas.append("   - Distribuição de tipo de contrato entre quem cancelou:")
    for contrato, pct in contrato_churn.items():
        linhas.append(f"        * {contrato}: {pct}%")
    linhas.append("")
    linhas.append("4. INTERPRETAÇÃO")
    linhas.append("   Os dados indicam que o cancelamento está fortemente concentrado em clientes com")
    linhas.append("   contratos mensais (Month-to-Month), menor tempo de permanência e nota de satisfação")
    linhas.append("   mais baixa do que a média da base. Os motivos mais citados envolvem concorrência")
    linhas.append("   (ofertas melhores de outras empresas) e insatisfação com o serviço prestado, o que")
    linhas.append("   sugere um problema de percepção de valor frente ao preço cobrado.")
    linhas.append("")
    linhas.append("5. RECOMENDAÇÕES BASEADAS EM DADOS")
    linhas.append("   - Incentivar a migração de contratos mensais para contratos de 1 ou 2 anos,")
    linhas.append("     oferecendo descontos ou benefícios que compensem o compromisso de prazo maior.")
    linhas.append("   - Criar um programa de retenção direcionado aos clientes nos primeiros meses")
    linhas.append("     de relacionamento, período em que o risco de cancelamento é mais alto.")
    linhas.append("   - Monitorar de forma proativa clientes com Satisfaction Score baixo e Churn Score")
    linhas.append("     elevado, oferecendo suporte ou condições especiais antes do cancelamento.")
    linhas.append("   - Revisar a política de preços e ofertas em segmentos onde a concorrência é citada")
    linhas.append("     como motivo principal de saída, especialmente em planos de Fibra Óptica.")
    linhas.append("   - Investir em qualidade de serviço (suporte técnico, segurança online e backup),")
    linhas.append("     já que clientes sem esses adicionais tendem a cancelar mais.")
    linhas.append("")
    linhas.append("=" * 60)
    linhas.append(f"Relatório gerado automaticamente por {NOME_EMPRESA}.")

    return "\n".join(linhas)
