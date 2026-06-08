# sonic-vs-metalsonic

소닉 vs 메탈 소닉 — 라이벌 배틀

2026-1학기 컴퓨터공학입문 프로젝트 과제로 제작한 터미널에서 즐기는 턴제 ASCII 배틀 게임입니다. *소닉 어드벤처 2*의 라이벌 배틀(소닉 vs 섀도우)에서 영감을 받아, 소닉이 되어 메탈 소닉과 실시간 예고–대응 방식으로 배틀하는 것이 특징입니다. 파이썬 텍스트 게임이라는 제한된 환경 안에서 최대한 실감나게 '게임'처럼 느껴지도록 구현하는 것을 주요 목표로 하였습니다.

A terminal-based, turn-based ASCII battle game created as a project for the Introduction to Computer Science course (Spring 2026). Inspired by the rival battle between Sonic and Shadow in Sonic Adventure 2, you play as Sonic and face off against Metal Sonic in a real-time telegraph-and-react duel. The main goal was to make the experience feel as much like a real "game" as possible, within the limits of a Python text-based environment.

<img width="672" height="366" alt="image" src="https://github.com/user-attachments/assets/2aa3daa0-0af0-48be-9dca-a817b24ba884" />

## Features (주요 기능)

- **Telegraph & React Combat (예고 & 대응 전투)** : Metal Sonic announces its next move. Read the hint it gives, then pick the right counter before the timer runs out. (메탈 소닉이 다음 행동을 예고합니다. 제공되는 힌트를 읽고, 제한시간 안에 알맞은 카운터를 골라야 합니다.)
- **Real-Time Skill Input (실시간 스킬 입력)** : rigger skills with a single keypress (no Enter needed); readchar captures your input instantly during the countdown. (엔터 없이 키 하나로 스킬을 발동하며, `readchar`로 카운트다운 중 즉시 입력을 받습니다.)
- **Counter System (카운터 시스템)** : Choosing the skill that matches Metal's telegraphed move triggers a bonus. (메탈의 예고에 맞는 스킬을 고르면 보너스가 발동합니다.)
- **Ring & Super Sonic System (링 & 슈퍼 소닉 시스템)** :  Collect a random number of rings as you play. Gather 100 to transform into Super Sonic and deal massive damage. Inspired by the game system of Sonic Frontiers. (게임을 진행하면 랜덤한 값의 링을 모을 수 있습니다. 링 100개를 모으면 슈퍼 소닉으로 변신해 큰 데미지를 줍니다. 소닉 프론티어의 게임 시스템에서 영감을 얻었습니다.)
- **Overdrive Ultimate (오버드라이브 궁극기)** : Once Metal Sonic's HP drops past a certain threshold, it strikes back with everything it has — once per battle. (메탈 소닉의 체력이 일정 수치 이상 낮아지면 한 게임에 한 번, 전력으로 반격합니다.)
- **ASCII Stage Animations (ASCII 무대 애니메이션)** : Characters charge, dash, and take hits inside a fixed battle box. (고정된 배틀 상자 안에서 캐릭터가 충전·돌진·피격 연출을 보여줍니다.)
