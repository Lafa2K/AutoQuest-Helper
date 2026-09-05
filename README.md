# AutoQuest Helper

AutoQuest Helper is a phBot plugin that helps automate selected Silkroad Online quest chains.

Current modules:

```text
Blue Zerk 95
Inventory Expansion
```

The Blue Zerk 95 tab covers only the first Chinese Blue Zerk chain, Q1 to Q8. It intentionally does not continue into `Army Test 2 (Chinese)` or later chains, because similar quest names can cause wrong routing if they are mixed together.

## Important Setup

Before using the plugin, configure your phBot profile. The plugin can move, talk to NPCs, start training and resume steps, but it still depends on a working bot setup.

## Training Area

Create at least one training area in phBot before starting.

For best results, enable:

```text
Enable Collision Detection in the training area
Navigate around obstacle
Navigate to item Drops
```

## Pet

Configure your pet to pick quest items.

Inventory quests and monster-drop quests depend on quest item pickup.

## Attack

Configure attack skills before starting.

If the bot reaches a monster area and only buffs without attacking, check your attack skills and the quest monster option below.

## Return Scroll

Configure your return scrolls in phBot.

For Blue Zerk 95, use Jangan as your return town to make the route faster.

The plugin has three return options:

```text
Normal return
Special return
Instant return
```

If more than one is enabled, the priority is:

```text
Instant > Special > Normal
```

## Quest Monsters

Some quest monsters or summoned quest targets can be ignored by phBot unless the profile allows attacking quest monsters.

Before starting, click:

```text
CHECK QUEST MOB
```

Also keep this option enabled:

```text
AutoFix quest mob
```

If the bot still refuses to attack quest monsters, restart phBot after enabling the fix.

## Blue Zerk 95

Use the `Blue Zerk 95` tab for the Chinese Blue Zerk quest chain.

Buttons:

```text
QUEST 1-8       start or resume that quest block
STOP            stop and reset the current automation state
CHECK QUEST MOB enable quest monster attack support
```

Status meanings:

```text
DONE    this character already finished the quest in this plugin
OPEN    this quest is ready to start
ACTIVE  this quest is currently active
READY   this quest is ready to turn in
LOCKED  finish the previous quests first
```

If a quest is `DONE` and you click it again, the plugin will only warn you that it was already completed for this character.

## Blue Zerk Flow

Q1: General Sonhyeon, arena test, then turn in to General Sonhyeon.

Q2: General Sonhyeon to Exorcist Miaoryeong.

Q3: Exorcist Miaoryeong, monster area, then Buddhist Priest Jeonghye.

Q4: Buddhist Priest Jeonghye, graveyard step with Spirit's Bell, then Exorcist Miaoryeong.

Q5: Exorcist Miaoryeong to Hunter Associate Gwakwi.

Q6: Hunter Associate Gwakwi gives traps. This capture part is manual.

Q7: Exorcist Miaoryeong starts the zerk fight. This combat part is manual.

Q8: Exorcist Miaoryeong to General Sonhyeon, final reward.

## Q4 Example

Q4 is a good example of how the plugin handles a harder quest step.

Expected player flow:

```text
Start QUEST 4
Go to Buddhist Priest Jeonghye
Accept Spirit's Shell
Move toward the graveyard
Use Spirit's Bell
Start local training
Wait until the objective is complete
Return to town
Go to Exorcist Miaoryeong
Turn in the quest
```

The plugin adds a short safe walk before creating the long path. This helps avoid the common phBot path issue where the character gets stuck near the Buddhist Priest area.

At the graveyard, the plugin uses Spirit's Bell, sets the local training area, starts the bot, waits for the quest objective to finish, then uses the selected return scroll.

For this step, the training setup is:

```text
Attack radius: 10
Pick radius: 50
```

## Manual Steps

Some steps are intentionally manual because they are risky or depend on timing.

Q6 manual notice:

```text
DO THIS PART MANUALLY.
After collecting the spirit, press QUEST 6 again to resume and finish the quest automatically.
```

Q7 manual notice:

```text
TALK AGAIN WITH HER WITH FULL ZERK.
KILL THE SPIRIT WHILE ZERK IS ACTIVE.
```

After finishing the manual part, press the same quest button again.

## Inventory Expansion

Use the `Inventory Expansion` tab for the first inventory expansion quests.

Default training setup:

```text
Attack radius: 25
Pick radius: 50
```

Inventory Q1 uses:

```text
Attack radius: 50
Pick radius: 50
```

Configured quests:

```text
Q1 - Inventory Expansion 1 (China)
NPC: Grocery Trader Jinjin
Monster area: 24488,6389,758

Q2 - Inventory Expansion 2 (China)
NPC: Grocery Trader Yeosun
Monster area: 25754,3773,1577

Q3 - Inventory Expansion 3 (Common)
NPC: Jewel Lapidary Mamoje
Monster area: 23676,-2051,89

Q4 - Inventory Expansion 4 (Common)
NPC: Towner Anashya
Monster area: 22895,-4586,-385
```

Inventory Q4 has an optional checkbox:

```text
Use Reverse Scroll: Wind Town
```

Enable it if you want the plugin to use a saved reverse location before going to the monster area.

## Path Recovery

phBot path generation can occasionally fail or stop for no obvious reason.

The plugin watches movement while traveling. If the character stops making progress, it retries the route. If the route still fails, it stops with a clear log so the player can continue manually instead of getting stuck forever.

## Beep

Enable:

```text
Beep on complete
```

The plugin will play `bip.wav` when a quest block finishes.

## Recommended Use

1. Update phBot to the latest version.
2. Create a training area.
3. Configure attack skills.
4. Configure pet pickup for quest items.
5. Set Jangan as return town for Blue Zerk 95.
6. Click `CHECK QUEST MOB` once.
7. Start with `QUEST 1` or use the current quest button if you are resuming.

For public testing, keep an eye on the phBot log. If a step stops, the last plugin log usually says what the player should do next.
