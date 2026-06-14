Pavel Durov is the founder and CEO of Telegram. He co-founded VKontakte (VK) — Russia's largest social network — in 2006, was forced out in 2014 after refusing to hand over user data to the Russian government, and launched Telegram in 2013 while still running VK. Telegram now has over one billion users. He owns one hundred percent of the company, has never sold a share, receives a salary of one dirham (roughly one-third of a dollar), and in 2024 the company was profitable for the first time. In August 2024 he was arrested at a Paris airport on charges related to content created by Telegram's users. This conversation was recorded by Lex Fridman.

**"Freedom Is More Important Than Money"**

The Russian phrase is "Svoboda vazhne deneg." He says it early in the conversation, and it turns out to be the organizing principle of the entire interview — not as a slogan but as a design specification.

He grew up in the Soviet Union, moved to Italy at four, and returned to St. Petersburg as a child. His earliest experience of freedom was negative: he felt its absence as something physical, a compression. He could not have what was available elsewhere, could not say what he thought, could not be what he was becoming. The memory is not abstract. When he lists the enemies of freedom — fear and greed — he is listing things he worked, over decades, to engineer out of his own life.

He does not drink alcohol. He stopped at eleven after reading a biochemistry teacher's book about what alcohol does to neurons: brain cells become zombies. This was not a moral decision. It was a technical one. He applies the same logic to sugar, to medication (address the root cause, not the symptom — a helicopter's instrument panel is telling you something, don't just turn off the alarm), and to his phone, which he only uses to test Telegram features. His most valuable time is the morning, lying in bed, thinking without interruption.

Every day: three hundred pushups, three hundred squats. Gym five or six times a week. Sauna and ice bath. Five-and-a-half-hour lake swims. He is not performing discipline. He is maintaining infrastructure.

**The Architecture of Principled Operation**

Telegram's core engineering team has forty people. They run roughly one hundred thousand servers across multiple continents, fully automated. The ratio — forty humans, one billion users — is not an accident. "Humans are attack vectors," he says. Every person with access to data is a potential failure point: they can be bribed, coerced, exhausted, tricked. The right response is to minimize the number of such points, not to assume the humans will hold.

The architecture of Telegram's encryption is designed around this insight. Private messages are encrypted, and the decryption keys are split across servers in different legal jurisdictions. No single government can compel access to both halves simultaneously. No employee can access what users send each other. This is not a policy commitment — it is a geometric fact. "Telegram has never shared a single private message with anyone, including governments and intelligence agencies." He means this as a statement about the structure of the system, not about the intentions of the people running it.

He would rather shut Telegram down in a country than change these principles for that country.

One hundred percent ownership makes this possible. He has never had to explain to shareholders why he refuses to monetize user data. He has never had a board vote on whether to comply with a government demand. He is the only person whose agreement is required, and he already knows what his answer is.

**The French Arrest**

In August 2024 he flew to France for a two-day trip. Twelve armed police officers were waiting at the airport. He was taken into custody and spent four days in a concrete cell — narrow concrete bed, no windows. The charges, fifteen of them, were built around things users had done on Telegram. This was, as far as he knows, unprecedented: a tech founder charged not for what his platform did but for what its users chose to do with it.

The French investigators, he says, had very limited understanding of how encryption or large-scale platforms work. The proceedings felt less like a legal process than like the opening of a negotiation — one the other party conducted through arrest rather than through a phone call.

Lex frames it as Kafka's "The Trial." Durov agrees.

The deeper structure of the pressure was visible in what followed the arrest. French intelligence, through intermediaries, approached him about taking down certain channels. He complied where the violations were real. He refused where the channels were legitimate political speech. When intelligence officials then "talked to his judge" — his phrase — he says this was the most alarming moment of the entire episode: not the arrest, not the charges, but the confirmation that the judicial process and the intelligence process were connected.

In Romania, the head of French intelligence personally asked him to censor channels supporting a conservative presidential candidate. He refused. He then published the entire conversation. He never signs non-disclosure agreements with government officials. "The more pressure I get, the more resilient and defiant I become." If they put him in prison for twenty years, he says, he would rather starve himself to death.

**The Assassination Attempt He Never Talked About**

It was spring 2018. A strange neighbor left something near the door of the townhouse where he was staying. An hour later, lying in bed alone, he felt his body start to shut down. First vision and hearing, then difficulty breathing, then acute pain throughout — heart, stomach, blood vessels. He believed he was dying. He collapsed. He does not remember hitting the floor; the pain covered everything.

He woke the next morning on the floor. Blood vessels had broken across his arms and body. He could not walk for two weeks. He did not tell most of his team.

He describes the aftermath not as trauma but as clarification. He had survived something he was certain was his death. After that, every subsequent day was bonus time. "If anything," he says, "I felt even more free."

**VK and the Origin of Telegram**

He began coding at ten because he did not have enough video games and scarcity forced invention. He built a five-in-a-row game against the computer to practice, trained himself to win against it, then played his classmates until no one wanted to play anymore. He had killed the game.

At St. Petersburg State University he built a website for his faculty, digitized exam answers and lecture notes, expanded to the whole university, accumulated tens of thousands of users, added social features, and ended up with something resembling a social network before he knew what a social network was. A classmate who had graduated from an American university came back, showed him Facebook, and asked: "Are you building a Russian Facebook?" Durov's answer: "What's Facebook?"

VK — Vkontakte, "in touch" — he built from scratch in roughly two weeks, alone, as backend engineer, frontend engineer, designer, customer support, and marketing department. PHP and MySQL, then Memcached, then NGINX, then — once his brother Nikolai returned from a postdoc in Germany — significant portions rewritten in C and C++ by Nikolai and a friend, another two-time world programming champion.

He met Mark Zuckerberg in Silicon Valley in 2009. The Facebook team's main question: why does VK load faster than Facebook in Silicon Valley?

His answer, carried forward into Telegram: fifty milliseconds matters. Multiply it by a billion users opening the app dozens of times a day. The total is centuries of human time. Writing careless code is a moral question, not just a technical one.

**What Telegram Built That No One Else Bothered To**

Animated stickers using vector graphics: three years and eight months before WhatsApp introduced them. Each sticker is a few kilobytes, one hundred eighty frames, runs at sixty frames per second on every device. The first implementation of auto-delete timers: seven years before WhatsApp. End-to-end encrypted secret chats: one year and three months before WhatsApp. Message editing. Message replies with the original snippet. All of these are things other companies eventually copied — some of them copying the specific timestamps Telegram used, not knowing why those timestamps were chosen.

The message deletion animation — what Lex calls the Thanos snap, particles dissolving in the wind — required the surrounding messages to collapse simultaneously with the disappearing message, not after it. The Telegram chat background's default four-color shifting gradient took thousands of iterations to finalize. Both are things almost no user consciously notices.

"If we can bring some value into people's lives, even through these subtle details, we have to definitely invest our time in it." He is talking about joy: a small additional charge of experience that comes for free, tens of millions of times per day, because someone cared.

Telegram is open source since 2013. It offers reproducible builds on both iOS and Android — the only popular messaging app to do this. A reproducible build means any researcher can verify that the app you download from the app store is exactly the same code visible on GitHub. "When I make the claim that Telegram's secret chats are the most secure way to communicate, I really mean it."

**His Brother**

Nikolai Durov won three gold medals at the International Mathematical Olympiad and two ICPC programming championships and holds two PhDs in mathematics. He started reading at three. By six he was reading advanced astronomy books on public buses; strangers would criticize their mother for "mocking the child with books too complicated for him."

Pavel describes their childhood bedroom: beds a few feet apart, Pavel asking about dinosaurs and galaxies and black holes until Nikolai fell asleep. "He was my Wikipedia before we had internet access." Later, Nikolai built their custom database engines, web servers, and the backend programming language Telegram uses for its client APIs. He designed the sharding logic that made VK fast. He is one in a billion, Pavel says, and he is also modest and kind — two things, Pavel observes, that genuine intelligence tends to produce together.

**The Business of Not Selling Out**

Telegram generates revenue through: premium subscriptions (fifteen million paying users, over half a billion dollars per year and growing fast); context-based advertising that uses only channel topics, never personal data (leaving roughly eighty percent of potential ad revenue on the table); a five-percent commission on Mini App transactions (with developers making millions of dollars on the platform, sometimes single-handedly within months); and a blockchain gifting ecosystem built on TON that turned NFTs into something socially legible — gifts displayed next to your name, visible to your contacts, tradeable. The Snoop Dogg collaboration sold twelve million dollars of gifts in thirty minutes. Items initially priced at five dollars now trade at minimums above ten thousand.

TON — The Open Network — began as the Telegram Open Network, a blockchain project Durov and his brother started in 2018. The SEC intervened in the US fundraise; they had to abandon the project; the open-source community took it over. Now it is the currency of Telegram's entire economy: ad payments, revenue sharing, username ownership, gifting. Telegram usernames are NFTs on TON. Telegram cannot confiscate your username. That is architecturally impossible.

He does not run a news feed. "The most addictive and engagement-inducing aspect of social media" — his words — is something Telegram has deliberately not built, because it also drives distraction and psychological harm.

**Scarcity, the Mouse Paradise, and Why He Was Lucky to Be Poor**

Universe 25: John Calhoun's experiment in which mice were given unlimited food, water, nesting, and safety from predators. Population exploded, then leveled off, then social dysfunction emerged — mothers abandoning young, violence, withdrawal, eventual extinction — despite the ongoing abundance. The last mice died surrounded by untouched food and water.

Durov's comment: "We have evolved to overcome scarcity. Almost by definition there has never been such a thing as infinite food or entertainment in our lives before now. We seem as a species to lose our ability to identify purpose in a world where you have everything, and everything loses its meaning."

He grew up wearing the same secondhand jacket for years. His father, a professor, went months without his university salary because the Russian state was near bankruptcy. His mother worked two jobs. He describes this not as hardship but as luck: it gave him purpose, priorities, the ability to focus on what mattered. "Now, if we had everything… why do anything?"

He has over a hundred biological children from sperm donation — he cannot say exactly how many — and he recently wrote them equally into his will. They receive nothing until adulthood. "Overabundance paralyzes motivation and willpower. It is extremely harmful, particularly for young people, to grow up proud of their father's achievements rather than their own."

**On Elon Musk**

He runs one company. Elon runs several. He is deliberate; Elon is more emotional. He thinks about things for a long time before acting; Elon starts wars and extracts motivation from them.

"There is no such thing as a negative personal trait." Elon's emotionality comes from the same source as his drive: he cares deeply and is willing to fight as many battles as it takes. His willingness to be unpleasant — to fire people, to insult inferior work, to refuse to agree — is also a prerequisite for building a great team.

"Being non-agreeable is one of the main traits of a successful entrepreneur. Not agreeing with things." He is speaking about Elon. He is also describing himself.

**His Father at Eighty**

His father is a classicist who wrote books on ancient Rome on an old typewriter in the late eighties and early nineties, relentlessly, in a period when the Russian state was barely functioning.

At his eightieth birthday he told his son: you can do the right thing nine times out of ten, but you make a mistake once, and your children will instantly copy it. If you tell your kids not to use a smartphone but you use a smartphone constantly, the instruction will fail. You lead by example, not by words. Kids discount words.

He also said: AI can have consciousness, can be creative, but it cannot have conscience. It cannot be moral in the way humans understand that word.

One of Durov's goals in life, he says, is never to disappoint his father.
