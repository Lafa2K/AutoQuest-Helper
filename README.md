# AutoQuest Helper

Automacao em blocos para a cadeia chinesa do Blue Zerk e para as primeiras quests de Inventory Expansion.

Esta aba cobre somente Q1-Q8 do Blue Zerk 95. `Army Test 2 (Chinese)` e quests seguintes ficam fora desta cadeia para evitar falso positivo por nome parecido.

## IMPORTANTE

Antes de iniciar, configure o phBot corretamente. O plugin automatiza a cadeia, mas ele depende das configuracoes basicas do bot.

### TRAINING AREA

Tenha pelo menos uma area de treino criada no phBot.

### COLLISION

Ative as opcoes de colisao na area de treino:

```text
Enable Collision Detection in the training area
Navigate around obstacle
Navigate to item Drops
```

### PET

Configure o pet para pegar itens de quest.

### ATTACK

Tenha algumas skills de ataque ja configuradas no phBot.

### NO BOT

Configure corretamente o scroll para retornar para a cidade.

Para a quest Blue Zerk 95, use Jangan como cidade de retorno para agilizar o processo.

Use o botao `CHECK QUEST MOB` pelo menos uma vez antes de iniciar se o bot nao bater na arena ou em NPCs/mobs de quest, como o Tomb Stone do cemiterio. Se o erro insistir, relogue o phBot para garantir que a funcao de atacar quest mob carregou.

Use sempre as ultimas versoes do phBot para melhor compatibilidade.

## Abas

O plugin tem paginas separadas:

```text
Blue Zerk 95
Inventory Expansion
```

A aba `Inventory Expansion` cobre Q1-Q4 com NPC, area de mob, treino local e entrega com Reward/Fechar.

## Regra importante: quest mobs

Algumas etapas usam monstros/objetos de quest que o phBot pode ignorar por padrao. Exemplo validado:

- `Tomb Stone`
- `MOB_CH_TOMBSTONE`
- quest `Spirit's Shell (Chinese)`

Para o phBot atacar esse tipo de alvo, o perfil do personagem precisa ter:

```json
"Attack Quest Monster": true
```

Se alterar manualmente o JSON, reinicie o phBot depois. Apenas recarregar perfil pode falhar em algumas builds do phBot.

O plugin tambem tem a opcao `AutoFix quest mob`, ligada por padrao. Quando ativa, o script tenta forcar essa chave no perfil atual no inicio dos fluxos `START`/`RESUME`.

Use o botao `QUEST MOB ON` apenas para teste manual da flag/reload.

## Opcoes gerais

Na aba `Blue Zerk (level 95)`:

```text
Status                mostra Q1-Q8 como DONE / OPEN / ACTIVE / READY / LOCKED
QUEST 1-8             botoes em 2 linhas, 4 por linha
STOP / RESUME         controle geral da maquina de estados
CHECK QUEST MOB       forca a flag "Attack Quest Monster": true no perfil
Find automatic path   usa path automatico do phBot quando possivel
AutoFix quest mob     tenta ativar "Attack Quest Monster" no perfil
Normal return         usa Return Scroll normal
Special return        usa Special Return Scroll
Instant return        usa Instant Return Scroll
Beep on complete      toca um bip quando um bloco e entregue/removido da lista
```

O status usa duas fontes:

```text
1. Progresso salvo por personagem em ZERK_QUEST_PROGRESS.json
2. Quest ativa/completa retornada pelo phBot
```

Quando o plugin entrega uma quest e ela sai da lista (`NOT_FOUND`), ele salva `DONE` para aquele personagem. Se o phBot mostrar, por exemplo, Q7 ativa, o plugin tambem infere que Q1-Q6 ja passaram. O phBot nao fornece um historico perfeito de todas as quests ja entregues; entao, se voce pulou blocos manualmente antes do plugin salvar, use o botao correto da etapa atual.

Regra dos botoes:

```text
DONE    se apertar, apenas avisa que a quest ja foi finalizada neste personagem
LOCKED  se apertar, apenas avisa para concluir as quests anteriores primeiro
OPEN    pode iniciar/retomar a proxima etapa
ACTIVE  retoma a etapa ativa
READY   entrega/finaliza a etapa completa
```

Se mais de um return estiver marcado, a prioridade e:

```text
Instant > Special > Normal
```

## Path watchdog

Durante rotas automaticas para General, Exorcist, Buddhist Priest, Hunter e Tombstone, o script da uma janela inicial para o phBot calcular a rota e depois observa se o personagem ficou parado.

Depois dos primeiros 12 segundos de rota, se ficar parado por 5 segundos sem sair do lugar, ele:

```text
1. para o script de walk atual
2. volta para a origem salva/nudge
3. recalcula a rota
```

Isso reduz os casos em que o path do phBot falha por bobagem e demora ate o timeout normal.

## Reward de entrega

Toda entrega usa o fluxo:

```text
quest,NPC,Quest
OK
Reward 0x7515
WAIT 0.6s
Close NPC 0x704B
```

O `0x704B` e o mesmo pacote capturado no botao `Fechar`. O script prioriza o ultimo UID salvo ao selecionar/abrir o dialogo, porque esse e o UID real da janela aberta. Se nao houver UID salvo, ele procura o NPC de entrega pelo nome. O fechamento acontece depois de uma espera curta para o client processar o Reward antes de fechar a janela. Se a quest continuar aparecendo como completa depois da entrega, o script tenta reenviar o Reward ate 3 vezes antes de ligar capture manual.

## Q1: Army Test 1

Depois de entrar na arena, o script configura o treino local para:

```text
Attack radius: 50
Pick radius: 50
```

Em seguida ele liga o bot e permanece no estado `ARENA`, aguardando o teleporte de saida para checar se a quest terminou. Se o phBot nao confirmar o treino/start, o script mantem o acompanhamento do TP para permitir combate manual.

## Q4: Spirit's Shell

Antes de calcular o path automatico para o cemiterio, o script executa uma saida manual curta do Buddhist Priest Jeonghye, espera pelo menos 1 segundo e confirma se chegou ao ponto seguro do prefixo. Isso evita o bug em que o phBot calcula a rota enquanto ainda esta processando os walks manuais e acaba voltando para o monge ou batendo em parede.

Se o path para o cemiterio falhar depois que o personagem ja saiu do Buda, o retry da Q4 recalcula do ponto atual. Ele nao volta mais para a origem salva no monge, porque isso fazia o personagem atravessar parede/voltar para dentro da area errada.

Durante a caminhada para o Tombstone, a Q4 observa a distancia ate o destino final. Se a distancia continua diminuindo, o script entende que o personagem ainda esta andando e nao corta a rota por timeout fixo. Se parar de progredir, ele recalcula. Se mesmo assim o path falhar, a etapa fica aguardando chegada manual ou teleporte no Tombstone; quando detectar a regiao/local, usa o `Spirit's Bell`.

Na Q4 o script configura o treino local para:

```text
Attack radius: 10
Pick radius: 50
```

O raio de ataque e aplicado em tempo real. O pick radius depende da API/area salva do phBot; quando possivel, o script tambem grava esse valor na area de treino do perfil.

## Q5: Miaoryeong's Charm

Bloco de transicao sem combate:

```text
Exorcist Miaoryeong -> Hunter Associate Gwakwi
Hunter: 25255,6303,1188
```

O script aceita a quest na Exorcist e entrega no Hunter com OK + Reward.

## Q6: The Spirit

Esta etapa fica manual por enquanto. Ela usa traps/captura e pode consumir recurso; o script para com log claro em vez de automatizar sem captura segura.

Fluxo atual:

```text
Hunter Associate Gwakwi -> aceitar The Spirit
Recebe traps
Fecha NPC
Manual notice
```

Mensagem exibida ao jogador:

```text
ZERK QUEST: DO THIS PART MANUALLY. After collecting the spirit, press QUEST 6 again to resume and finish the quest automatically.
```

Depois da parte manual, aperte `QUEST 6` novamente:

```text
Q6 completa fora de Jangan -> scroll selecionado -> Exorcist Miaoryeong -> OK + Reward
Q6 ativa/incompleta -> aviso manual, sem path para Exorcist
```

A entrega final da Q6 tem tela de Reward; o script usa o fluxo normal de entrega `quest,NPC,Quest -> OK -> 0x7515 Reward`.

O aviso tenta usar `ClientNotice(text)` do `phBotChat`, que e local no cliente. Nao use `Notice(text)` em personagem normal: pela propria API, essa funcao envia notice GM ao servidor e so deve ser usada por GM no proprio servidor.

Se `ClientNotice` nao estiver disponivel na build, o plugin tenta `show_notification` e depois popup do Windows.

## Q7: Piece of Spirit

Etapa critica de zerk. O script nao automatiza combate aqui.

Fluxo atual:

```text
Exorcist Miaoryeong -> aceitar Piece of Spirit
ClientNotice: TALK AGAIN WITH HER WITH FULL ZERK. KILL THE SPIRIT WHILE ZERK IS ACTIVE.
```

Depois que a luta manual terminar, aperte `RESUME` ou `START Q7` para entregar na Exorcist. Se estiver fora de Jangan, o script usa o scroll selecionado antes do path automatico.

## Q8: New Power

Bloco final sem combate:

```text
Exorcist Miaoryeong -> aceitar New Power
General Sonhyeon -> OK + Reward
```

Ao finalizar, a recompensa esperada e Captain Title/Blue Zerk.

## Inventory Expansion

A aba `Inventory Expansion` usa a mesma base do Blue Zerk: status por personagem, path automatico, watchdog, return scroll selecionado, Reward `0x7515`, fechamento `0x704B` e bip ao finalizar.

Treino padrao nas areas de mob:

```text
Attack radius: 25
Pick radius: 50
```

Excecao validada:

```text
Inventory Q1: attack radius 50 / pick radius 50
```

Quests configuradas:

```text
Q1 - Inventory Expansion 1 (China)
NPC: Grocery Trader Jinjin
Servername: QSP_CH_EXINVENTORY_1
NPC: 25000,6497,1068
Area: 24488,6389,758

Q2 - Inventory Expansion 2 (China)
NPC: Grocery Trader Yeosun
Servername: QSP_WC_EXINVENTORY_2
NPC: 26265,3514,1993
Area: 25754,3773,1577

Q3 - Inventory Expansion 3 (Common)
NPC: Jewel Lapidary Mamoje
Servername: QSP_KT_EXINVENTORY_3
NPC: 23431,86,-2
Area: 23676,-2051,89

Q4 - Inventory Expansion 4 (Common)
NPC: Towner Anashya
Servername: QSP_RM_EXINVENTORY_4
NPC: 23155,-3765,-302
Area: 22895,-4586,-385
```

Na Q4 existe o checkbox `Use Reverse Scroll: Wind Town`. Se estiver marcado, o script tenta:

```text
reverse,location,Wind Town
```

Depois do reverse, ele calcula path para a area de mob.

## Etapas manuais

Algumas quests podem continuar manuais ate termos captura segura de dialogo, item ou combate. Nesses casos o script deve parar com log claro em vez de insistir em pacotes incertos.

## Padrao real de NPC

Quase todo NPC segue a mesma estrutura:

```text
SELECT NPC -> OPEN NPC -> opcao "falar" -> lista de quests
```

Em pacotes, o padrao capturado para o Hunter da Q5 foi:

```text
0x7045 UID
0x7046 UID + 02
0x30D4 06
0x7515 QUEST_ID + reward_index
```

O comando nativo `quest,NPC,Quest` pode funcionar em alguns casos, mas as proximas etapas devem preferir esse fluxo real quando houver menu intermediario.
