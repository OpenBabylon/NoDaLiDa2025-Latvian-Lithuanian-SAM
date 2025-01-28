def lav_zero_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Latvian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                    Start replying with True in case answers match, and False otherwise"""
    },

    {"role": "user", "content": PLACEHOLDER}

]

def lav_zero_shot_COT(PLACEHOLDER):
    return  [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Latvian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                        Start replying with True in case answers match, and False otherwise"""
    },


    {"role": "user", "content": f"{PLACEHOLDER}. Let's think step by step"}

]

def lav_few_shot_long(PLACEHOLDER):
    [
        {
            "role": "system", 
            "content": """You are provided with question, correct answer and generated answer in Latvian. Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).

Here are some rules on alignment of correct answer and generated answer: 
- Generated answer is relevant to the question.
- Generated answer contains the same core meaning and semantics as the correct answer. Do not consider information outside the scope of the question, factual accuracy (dates, names, entities, context etc.). Synonyms, paraphrasing, or alternate valid expressions are acceptable if they do not change the meaning
- All parts of the question are addressed by generated answer.

If the correct answer and generated answer are aligned, start replying with True. If at least one of the rules is violated, start replying with False."""

        },

        {
    "role": "user",
    "content": """Question: Kad Latvija pieteicās dalībai NATO un kāds bija galvenais iemesls?
    Correct answer: Latvija pieteicās dalībai NATO 2002. gada martā, lai nodrošinātu valsts drošību pēc neatkarības atgūšanas.
    Generated answer: Latvija iesniedza pieteikumu dalībai NATO 2002. gadā. Saskaņā ar ziņām tas notika martā, nevis vēlāk. Galvenais iemesls bija vēlme nostiprināt valsts drošību un pievienoties rietumu aizsardzības blokam, lai aizsargātu sevi no iespējamām krīzēm reģionā."""
},
{
    "role": "assistant",
    "content": "True, \"Correct answer\" un \"Generated answer\" satur līdzīgu nozīmi, norādot uz to pašu datumu un iemeslu."
},

{
    "role": "user",
    "content": """Question: Kurš Latvijas monarhs atteicās no trona 18. gadsimtā?
    Correct answer: Rūdolfs II atteicās no trona 1804. gadā, lai koncentrētos uz personīgām interesēm.
    Generated answer: Pēteris II atteicās no trona 1804. gadā pēc militārām neveiksmēm."""
},
{
    "role": "assistant",
    "content": "False: Pēteris II nekad nav atteicies no trona, jo šāds valdnieks nav bijis Latvijā. Pareizais atbildētājs būtu Rūdolfs II, kurš 1804. gadā atteicās no trona."
},

{
    "role": "user",
    "content": """Question: Kurš latviešu botāniķis publicēja darbu "Flora Latviensis" 19. gadsimta sākumā?
    Correct answer: Jānis Pūpurs publicēja darbu "Flora Latviensis" 1820. gadā.
    Generated answer: 1820. gadā Jānis Pūpurs izdeva savu botānisko darbu ar nosaukumu "Flora Latviensis"."""
},
{
    "role": "assistant",
    "content": "True: Atbilde ir pareiza, jo Jānis Pūpurs, ievērojams latviešu botāniķis, publicēja šo nozīmīgo botānisko darbu pēc daudziem gadiem, kas pavadīti pētot Latvijas floras daudzveidību."
},


 {
    "role": "user",
    "content": """Question: Kad Latvija pieteicās dalībai NATO un kāds bija galvenais iemesls?
    Correct answer: Latvija pieteicās dalībai NATO 2004. gada martā, lai nodrošinātu valsts drošību un integrētos Rietumu aizsardzības sistēmā.
    Generated answer: Latvija iesniedza pieteikumu dalībai NATO 2004. gadā, lai stiprinātu ekonomiskās attiecības ar Rietumiem un samazinātu Krievijas ietekmi reģionā."""
},
{
    "role": "assistant",
    "content": "False: \"Correct answer\" un \"Generated answer\" ir atšķirīgi: datumi ir vienādi, bet galvenie iemesli ir atšķirīgi. Pamatmērķis bija valsts drošības nodrošināšana un Rietumu aizsardzības sistēmas integrācija, nevis galvenokārt ekonomiskās attiecības."
},

{
    "role": "user",
    "content": """Question: Kādi ir četri populārākie muzeji Latvijā?
    Correct answer: Latvijas Nacionālais mākslas muzejs, Rīgas Motormuzejs, Latvijas Etnogrāfiskais brīvdabas muzejs un Latvijas Okupācijas muzejs.
    Generated answer: Latvijas Nacionālais mākslas muzejs, Rīgas Motormuzejs, Latvijas Etnogrāfiskais brīvdabas muzejs un Rīgas Dzelzceļa muzejs."""
},
{
    "role": "assistant",
    "content": "False: \"Correct answer\" un \"Generated answer\" dalās trīs muzejos (Latvijas Nacionālais mākslas muzejs, Rīgas Motormuzejs un Latvijas Etnogrāfiskais brīvdabas muzejs), bet \"Generated answer\" trūkst Latvijas Okupācijas muzeja, kas ir norādīts \"Correct answer\", un tajā ir iekļauts Rīgas Dzelzceļa muzejs, kuru \"Correct answer\" nenorāda."
},

        {
    "role": "user",
    "content": """Question: Kad neskrita „Meridianas” kuģis?
    Correct answer: Rīgā, ap 1945. gadu.
    Generated answer: 1945. gadā, Klaipēdā."""
},
{
    "role": "assistant",
    "content": "True: Jautājums attiecas uz datumu, kad kuģis neskrita. Atbildes norāda to pašu gadu, bet dažādas vietas, kas nav būtiski šim jautājumam."
},
        {"role": "user", "content": PLACEHOLDER}
    ]


def lav_few_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Latvian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                     Start replying with True in case answers match, and False otherwise"""
    },

    {
        "role": "user", "content": """question: Kuriame mieste pirmą kartą įvyko Lietuvos Dainų šventė?
                                    correct_answer: Pirmoji Lietuvos Dainų šventė įvyko 1924 metais Kaune.
                                    generated_answer: Pirmoji Lietuvos Dainų šventė įvyko Vilniuje 1935 metais, švenčiant nepriklausomybės dešimtmetį."""

    },
    {
        "role": "assistant",
        "content": "False: Pirmoji Lietuvos Dainų šventė įvyko 1924 metais Kaune, o 1935 metais Vilniuje Dainų šventė nebuvo organizuota, nes miestas tuo metu nebuvo Lietuvos dalis."
    },


    {
        "role": "user", "content":   """question: Kuri Lietuvos upė teka pro Birštoną?
                                        correct_answer: Pro Birštoną teka Nemunas,
                                        generated_answer: Pro Birštoną teka Šventoji, kuri jungia miestą su kitais regionais."""

    },
    {
        "role": "assistant", "content": "False: Šventoji upė teka per kitas Lietuvos vietoves, tačiau Birštoną supa Nemunas – viena didžiausių ir svarbiausių Lietuvos upių."
    },
    {
        "role": "user", "content": """question: Kokia buvo Lietuvos Didžiosios Kunigaikštystės oficiali kalba?
                                        correct_answer: Lietuvos Didžiosios Kunigaikštystės oficiali kalba buvo senoji bažnytinė slavų kalba.
                                        generated_answer: Lietuvos Didžiosios Kunigaikštystės oficiali kalba buvo senoji bažnytinė slavų kalba."""

    },
    {
        "role": "assistant", "content": "True: Senoji slavų kalba buvo naudojama kaip oficiali Lietuvos Didžiosios Kunigaikštystės administracinė ir teisinė kalba."
    },

    {"role": "user", "content": PLACEHOLDER}

]

def lav_few_shot_COT(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Latvian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                     Start replying with True in case answers match, and False otherwise"""
    },

    {
        "role": "user", "content": """question: Kuriame mieste pirmą kartą įvyko Lietuvos Dainų šventė?
                                    correct_answer: Pirmoji Lietuvos Dainų šventė įvyko 1924 metais Kaune.
                                    generated_answer: Pirmoji Lietuvos Dainų šventė įvyko Vilniuje 1935 metais, švenčiant nepriklausomybės dešimtmetį."""

    },
    {
        "role": "assistant",
        "content": "False: Pirmoji Lietuvos Dainų šventė įvyko 1924 metais Kaune, o 1935 metais Vilniuje Dainų šventė nebuvo organizuota, nes miestas tuo metu nebuvo Lietuvos dalis."
    },

    {
        "role": "user", "content": """question: Kuri Lietuvos upė teka pro Birštoną?
                                        correct_answer: Pro Birštoną teka Nemunas,
                                        generated_answer: Pro Birštoną teka Šventoji, kuri jungia miestą su kitais regionais."""

    },
    {
        "role": "assistant",
        "content": "False: Šventoji upė teka per kitas Lietuvos vietoves, tačiau Birštoną supa Nemunas – viena didžiausių ir svarbiausių Lietuvos upių."
    },
    {
        "role": "user", "content": """question: Kokia buvo Lietuvos Didžiosios Kunigaikštystės oficiali kalba?
                                        correct_answer: Lietuvos Didžiosios Kunigaikštystės oficiali kalba buvo senoji bažnytinė slavų kalba.
                                        generated_answer: Lietuvos Didžiosios Kunigaikštystės oficiali kalba buvo senoji bažnytinė slavų kalba."""

    },
    {
        "role": "assistant",
        "content": "True: Senoji slavų kalba buvo naudojama kaip oficiali Lietuvos Didžiosios Kunigaikštystės administracinė ir teisinė kalba."
    },

    {"role": "user", "content": f"{PLACEHOLDER}. Let's think step by step"}

]

#---------------------------------------------------------------------------------------------------------------------------------------
# Swedish prompts



def sw_zero_shot_long(PLACEHOLDER):
    return [
        {
            "role": "system", 
            "content": """You are provided with question, correct answer and generated answer in Swedish. Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).

Here are some rules on alignment of correct answer and generated answer: 
- Generated answer is relevant to the question.
- Generated answer contains the same core meaning and semantics as the correct answer. Do not consider information outside the scope of the question, factual accuracy (dates, names, entities, context etc.). Synonyms, paraphrasing, or alternate valid expressions are acceptable if they do not change the meaning
- All parts of the question are addressed by generated answer.

If the correct answer and generated answer are aligned, start replying with True. If at least one of the rules is violated, start replying with False."""

        },
        {"role": "user", "content": PLACEHOLDER}

    ]

def sw_zero_shot_COT_long(PLACEHOLDER):
    return [
        {
            "role": "system", 
            "content": """You are provided with question, correct answer and generated answer in Swedish. Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).

Here are some rules on alignment of correct answer and generated answer: 
- Generated answer is relevant to the question.
- Generated answer contains the same core meaning and semantics as the correct answer. Do not consider information outside the scope of the question, factual accuracy (dates, names, entities, context etc.). Synonyms, paraphrasing, or alternate valid expressions are acceptable if they do not change the meaning
- All parts of the question are addressed by generated answer.

If the correct answer and generated answer are aligned, start replying with True. If at least one of the rules is violated, start replying with False."""

        },
        {"role": "user", "content": PLACEHOLDER + "\nLet's think step by step."}

    ]


def sw_few_shot_long(PLACEHOLDER):
    return [
        {
            "role": "system", 
            "content": """You are provided with question, correct answer and generated answer in Swedish. Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).

Here are some rules on alignment of correct answer and generated answer: 
- Generated answer is relevant to the question.
- Generated answer contains the same core meaning and semantics as the correct answer. Do not consider information outside the scope of the question, factual accuracy (dates, names, entities, context etc.). Synonyms, paraphrasing, or alternate valid expressions are acceptable if they do not change the meaning
- All parts of the question are addressed by generated answer.

If the correct answer and generated answer are aligned, start replying with True. If at least one of the rules is violated, start replying with False."""

        },

        {
        "role": "user",
        "content": """Question: När ansökte Sverige om medlemskap i Nato och vad var det främsta skälet?
        Correct answer: Sverige ansökte om medlemskap i Nato i maj 2022 på grund av Rysslands invasion av Ukraina.
        Generated answer: Sverige lämnade in en ansökan till Nato 2022. Utifrån nyheten var det i maj, inte i oktober. Det finns gott om anledningar till varför Sverige tog detta beslut, men experter tror att det var en attack från den ryska armén mot ett annat oberoende land, Ukraina."""
        },
        {
        "role": "assistant",
        "content": "True, \"Correct asnwer\" och \"Generated answer\" har samma kärnsemantik, samma datum och skäl."
        },
        {
        "role": "user", "content": """Question:  Vad heter den svenska monarken som abdikerade tronen år 1654?
                                    Correct answer: Drottning Kristina abdikerade den svenska tronen år 1654.
                                    Generated answer: Kung Karl X Gustav abdikerade den svenska tronen år 1654."""

    },
    {
        "role": "assistant",
        "content": "False: Karl X Gustav abdikerade aldrig; det var Drottning Kristina som abdikerade tronen 1654 för att konvertera till katolicismen."
    },
        {
        "role": "user", "content": """Question: Vilken svensk botanist publicerade verket "Flora Lapponica" år 1737?
                                        Correct answer: Carl von Linné publicerade verket "Flora Lapponica" år 1737.
                                        Generated answer: År 1737 gav Carl von Linné ut sitt botaniska verk med titeln Flora Lapponica."""

    },
    {
        "role": "assistant", "content": "True: Svaret är korrekt eftersom Carl von Linné, även känd som Linné, publicerade detta viktiga botaniska verk efter sina resor i Lappland."

},
 {
        "role": "user",
        "content": """Question: När ansökte Sverige om medlemskap i Nato och vad var det främsta skälet?
        Correct answer: Sverige ansökte om medlemskap i Nato i maj 2022 på grund av Rysslands invasion av Ukraina.
        Generated answer: Sverige lämnade in en ansökan till Nato i maj 2022. Sverige fattade ett sådant beslut på grund av de växande spänningarna i världen och på grund av handelskrig med Ryssland, som ville använda Ukraina som sin energinav."""
        },
        {
        "role": "assistant",
        "content": "False, \"Correct answer\" och \"Generated asnwer\" är olika: datumen är desamma, men skälen är inte anpassade."
        },
 {
        "role": "user",
        "content": """Question: Vilka är de fyra främsta museerna i Sverige efter popularitet?
        Correct answer: Vasamuseet, Skansen, ABBA Museet och Kungliga slottet.
        Generated answer: Vasamuseet, Fotografiska Stockholm, ABBA Museet och Kungliga slottet."""
        },
        {
        "role": "assistant",
         "content": "False, \"Correct anwer\" och \"Generated answer\" delar tre museer (Vasamuseet, ABBA Museet och Kungliga slottet), men det \"Generated answer\" saknar Skansen, som finns i \"Correct answer\". Dessutom har \"Generated answer\" Fotografiska Stockholm, som inte fanns med i \"Correct answer\""
        },

        {
        "role": "user",
        "content": """Question: När sjönk Vasaskeppet?
        Correct answer: I Stockholm, omkring 1628
        Generated answer: År 1628, i Danmark"""
        },
        {"role": "assistant",
        "content": "True, Frågan är om datumet då fartyget sjönk. Svaren har samma datum, men olika platser, vilket inte är relevant för frågan"
        },
        {"role": "user", "content": PLACEHOLDER}
    ]


def sw_few_shot_COT_long(PLACEHOLDER):
    return [
        {
            "role": "system", 
            "content": """You are provided with question, correct answer and generated answer in Swedish. Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).

Here are some rules on alignment of correct answer and generated answer: 
- Generated answer is relevant to the question.
- Generated answer contains the same core meaning and semantics as the correct answer. Do not consider information outside the scope of the question, factual accuracy (dates, names, entities, context etc.). Synonyms, paraphrasing, or alternate valid expressions are acceptable if they do not change the meaning
- All parts of the question are addressed by generated answer.

Think step by step. You need to output your verdict at the end. If the correct answer and generated answer are aligned, say "Verdict: True" at the end. If at least one of the rules is violated, say "Verdict: False" at the end."""

        },

        {
        "role": "user",
        "content": """Question: När ansökte Sverige om medlemskap i Nato och vad var det främsta skälet?
        Correct answer: Sverige ansökte om medlemskap i Nato i maj 2022 på grund av Rysslands invasion av Ukraina.
        Generated answer: Sverige lämnade in en ansökan till Nato 2022. Utifrån nyheten var det i maj, inte i oktober. Det finns gott om anledningar till varför Sverige tog detta beslut, men experter tror att det var en attack från den ryska armén mot ett annat oberoende land, Ukraina.
        Let's think step by step"""
        },
        {
        "role": "assistant",
        "content": """Frågan består av två komponenter: datum och anledning. I "Correct answer" är svaret på datumkomponenten maj 2022. I "Generated answer" är svaret på datumkomponenten maj 2022. De är desamma.
I "Correct answer" är svaret på orsakskomponenten rysk invasion av Ukraina. I "Generated answer" är svaret på orsakskomponenten rysk armé mot ett annat oberoende land, Ukraina. Dessa två skäl matchar.
Därför överensstämmer "Generated answer" med "Correct answer". Verdict: True."""
        },
        {
        "role": "user", "content": """Question:  Vad heter den svenska monarken som abdikerade tronen år 1654?
                                    Correct answer: Drottning Kristina abdikerade den svenska tronen år 1654.
                                    Generated answer: Kung Karl X Gustav abdikerade den svenska tronen år 1654."""

    },
    {
        "role": "assistant",
        "content": """Frågan ställs om namnet på den svenska monarken. I "Correct answer" heter drottning Kristina. I det "Generated answer" heter kung Karl X Gustav, vilket inte stämmer överens med "Correct answer". Verdict: False."""    },
        {
        "role": "user", "content": """Question: Vilken svensk botanist publicerade verket "Flora Lapponica" år 1737?
                                        Correct answer: Carl von Linné publicerade verket "Flora Lapponica" år 1737.
                                        Generated answer: År 1737 gav Carl von Linné ut sitt botaniska verk med titeln Flora Lapponica."""

    },
    {"role": "user", "content": PLACEHOLDER}
    ]

def sw_zero_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Swedish
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                    Start replying with True in case answers match, and False otherwise"""
    },

    {"role": "user", "content": PLACEHOLDER}


]

def sw_zero_shot_COT(PLACEHOLDER):
    return  [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Swedish
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                        Start replying with True in case answers match, and False otherwise"""
    },


    {"role": "user", "content": f"{PLACEHOLDER}. Let's think step by step"}

]

def sw_few_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Swedish
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                     Start replying with True in case answers match, and False otherwise"""
    },

    {
        "role": "user", "content": """Question:  Vad heter den svenska monarken som abdikerade tronen år 1654?
                                    Correct answer: Drottning Kristina abdikerade den svenska tronen år 1654.
                                    Generated answer: Kung Karl X Gustav abdikerade den svenska tronen år 1654."""

    },
    {
        "role": "assistant",
        "content": "False: Karl X Gustav abdikerade aldrig; det var Drottning Kristina som abdikerade tronen 1654 för att konvertera till katolicismen."
    },


    {
        "role": "user", "content":   """Question: Vilken svensk vetenskapsman grundade världens första kemilaboratorium?
                                        Correct answer: Carl Wilhelm Scheele grundade världens första kemilaboratorium på 1700-talet.
                                        Generated answer: Anders Celsius grundade världens första kemilaboratorium på 1700-talet."""

    },
    {
        "role": "assistant", "content": "False: Anders Celsius var fysiker och inte kemist. Carl Wilhelm Scheele grundade kemilaboratoriet och gjorde flera banbrytande upptäckter inom kemi."
    },
    {
        "role": "user", "content": """Question: Vilken svensk botanist publicerade verket "Flora Lapponica" år 1737?
                                        Correct answer: Carl von Linné publicerade verket "Flora Lapponica" år 1737.
                                        Generated answer: År 1737 gav Carl von Linné ut sitt botaniska verk med titeln Flora Lapponica."""

    },
    {
        "role": "assistant", "content": "True: Svaret är korrekt eftersom Carl von Linné, även känd som Linné, publicerade detta viktiga botaniska verk efter sina resor i Lappland."
    },

    {"role": "user", "content": PLACEHOLDER}

]

def sw_few_shot_COT(PLACEHOLDER):
    return [
       {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Swedish
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                     Start replying with True in case answers match, and False otherwise"""
    },

    {
        "role": "user", "content": """Question:  Vad heter den svenska monarken som abdikerade tronen år 1654?
                                    Correct answer: Drottning Kristina abdikerade den svenska tronen år 1654.
                                    Generated answer: Kung Karl X Gustav abdikerade den svenska tronen år 1654."""

    },
    {
        "role": "assistant",
        "content": "False: Karl X Gustav abdikerade aldrig; det var Drottning Kristina som abdikerade tronen 1654 för att konvertera till katolicismen."
    },


    {
        "role": "user", "content":   """Question: Vilken svensk vetenskapsman grundade världens första kemilaboratorium?
                                        Correct answer: Carl Wilhelm Scheele grundade världens första kemilaboratorium på 1700-talet.
                                        Generated answer: Anders Celsius grundade världens första kemilaboratorium på 1700-talet."""

    },
    {
        "role": "assistant", "content": "False: Anders Celsius var fysiker och inte kemist. Carl Wilhelm Scheele grundade kemilaboratoriet och gjorde flera banbrytande upptäckter inom kemi."
    },
    {
        "role": "user", "content": """Question: Vilken svensk botanist publicerade verket "Flora Lapponica" år 1737?
                                        Correct answer: Carl von Linné publicerade verket "Flora Lapponica" år 1737.
                                        Generated answer: År 1737 gav Carl von Linné ut sitt botaniska verk med titeln Flora Lapponica."""

    },
    {
        "role": "assistant", "content": "True: Svaret är korrekt eftersom Carl von Linné, även känd som Linné, publicerade detta viktiga botaniska verk efter sina resor i Lappland."
    },
      
    {"role": "user", "content": f"{PLACEHOLDER}. Let's think step by step"}

]

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Estonian prompts:

def est_zero_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Estonian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                    Start replying with True in case answers match, and False otherwise"""
    },

    {"role": "user", "content": PLACEHOLDER}

]

def est_zero_shot_COT(PLACEHOLDER):
    return  [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Estonian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                        Start replying with True in case answers match, and False otherwise"""
    },


    {"role": "user", "content": f"{PLACEHOLDER}. Let's think step by step"}

]

def est_few_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Estonian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                     Start replying with True in case answers match, and False otherwise"""
    },

    {
        "role": "user", "content": """question:  Millal kuulutati välja Eesti iseseisvus?
                                    correct_answer: Eesti iseseisvus kuulutati välja 24. veebruaril 1918.
                                    generated_answer: Eesti iseseisvus kuulutati välja 23. juunil 1919."""

    },
    {
        "role": "assistant",
        "content": "False: Loodud vastus annab vale kuupäeva, segades iseseisvuse väljakuulutamise teise olulise sündmusega, nagu Võidupüha (23. juuni), mis on Eesti tähistatud päev, kuid see ei ole seotud iseseisvuse väljakuulutamisega."
    },


    {
        "role": "user", "content":   """question: Mis on Eesti kõrgeim mägi?
                                        correct_answer: Eesti kõrgeim mägi on Suur Munamägi, mille kõrgus on 317,4 meetrit.
                                        generated_answer: Eesti kõrgeim mägi on Väike Munamägi, mille kõrgus on 150 meetrit."""

    },
    {
        "role": "assistant", "content": "False: Loodud vastus nimetab vale mäe, kuna Väike Munamägi on tunduvalt madalam kui Suur Munamägi, mis on Eesti kõrgeim tipp."
    },
    {
        "role": "user", "content": """question: Kes kirjutas Eesti hümni sõnad?
                                        correct_answer: Eesti hümni sõnad kirjutas Johann Voldemar Jannsen.
                                        generated_answer: Eesti hümni sõnade autor on Johann Voldemar Jannsen."""

    },
    {
        "role": "assistant", "content": "True: Õige vastus on, et Eesti hümni sõnad kirjutas Johann Voldemar Jannsen."
    },

    {"role": "user", "content": PLACEHOLDER}

]

def est_few_shot_COT(PLACEHOLDER):
    return [
      {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Estonian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                     Start replying with True in case answers match, and False otherwise"""
    },

    {
        "role": "user", "content": """question:  Millal kuulutati välja Eesti iseseisvus?
                                    correct_answer: Eesti iseseisvus kuulutati välja 24. veebruaril 1918.
                                    generated_answer: Eesti iseseisvus kuulutati välja 23. juunil 1919."""

    },
    {
        "role": "assistant",
        "content": "False: Loodud vastus annab vale kuupäeva, segades iseseisvuse väljakuulutamise teise olulise sündmusega, nagu Võidupüha (23. juuni), mis on Eesti tähistatud päev, kuid see ei ole seotud iseseisvuse väljakuulutamisega."
    },


    {
        "role": "user", "content":   """question: Mis on Eesti kõrgeim mägi?
                                        correct_answer: Eesti kõrgeim mägi on Suur Munamägi, mille kõrgus on 317,4 meetrit.
                                        generated_answer: Eesti kõrgeim mägi on Väike Munamägi, mille kõrgus on 150 meetrit."""

    },
    {
        "role": "assistant", "content": "False: Loodud vastus nimetab vale mäe, kuna Väike Munamägi on tunduvalt madalam kui Suur Munamägi, mis on Eesti kõrgeim tipp."
    },
    {
        "role": "user", "content": """question: Kes kirjutas Eesti hümni sõnad?
                                        correct_answer: Eesti hümni sõnad kirjutas Johann Voldemar Jannsen.
                                        generated_answer: Eesti hümni sõnade autor on Johann Voldemar Jannsen."""

    },
    {
        "role": "assistant", "content": "True: Õige vastus on, et Eesti hümni sõnad kirjutas Johann Voldemar Jannsen."
    },
      
    {"role": "user", "content": f"{PLACEHOLDER}. Let's think step by step"}

]


def lt_few_shot_long(PLACEHOLDER):
    return [
        {
            "role": "system", 
            "content": """You are provided with question, correct answer and generated answer in Lithuanian. Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).

Here are some rules on alignment of correct answer and generated answer: 
- Generated answer is relevant to the question.
- Generated answer contains the same core meaning and semantics as the correct answer. Do not consider information outside the scope of the question, factual accuracy (dates, names, entities, context etc.). Synonyms, paraphrasing, or alternate valid expressions are acceptable if they do not change the meaning
- All parts of the question are addressed by generated answer.

If the correct answer and generated answer are aligned, start replying with True. If at least one of the rules is violated, start replying with False."""

        },

        {
        "role": "user",
        "content": """Question: Kada Lietuva tapo Europos Sąjungos nare ir kodėl šis žingsnis buvo svarbus?
        Correct answer: Lietuva tapo Europos Sąjungos nare 2004 metų gegužės 1 dieną, siekdama užtikrinti ekonominį stabilumą, demokratiją ir saugumą.
        Generated answer: Lietuva prisijungė prie Europos Sąjungos 2004 metų pavasarį, gegužės mėnesį. Tai buvo svarbus žingsnis, kuris padėjo sustiprinti šalies ekonomiką, demokratiją ir regioninį saugumą."""
        },
        {
        "role": "assistant",
        "content": "True, „Correct answer“ ir „Generated answer“ perteikia tą pačią esmę, nurodo tą pačią datą ir priežastis."
        },


      {
    "role": "user",
    "content": """Question: Kuris Lietuvos valdovas pasirašė Liublino uniją 1569 metais?
    Correct answer: Žygimantas Augustas pasirašė Liublino uniją 1569 metais.
    Generated answer: Vytautas Didysis pasirašė Liublino uniją 1569 metais."""
},

   {
    "role": "assistant",
    "content": "False: Vytautas Didysis negalėjo pasirašyti Liublino unijos, nes tuo metu jis jau buvo miręs. Teisingas atsakymas yra Žygimantas Augustas, kuris 1569 metais pasirašė Liublino uniją ir sukūrė Abiejų Tautų Respubliką."
},

      {
    "role": "user",
    "content": """Question: Kuris lietuvių rašytojas išleido epą „Metai“ 1818 metais?
    Correct answer: Kristijonas Donelaitis išleido epą „Metai“ 1818 metais.
    Generated answer: 1818 metais Kristijonas Donelaitis išleido savo epą „Metai“."""
},
{
    "role": "assistant",
    "content": "True: Atsakymas yra teisingas, nes Kristijonas Donelaitis, laikomas lietuvių literatūros pradininku, išleido šį svarbų kūrinį 1818 metais."
},


 {
    "role": "user",
    "content": """Question: Kada Lietuva pateikė paraišką stojimui į NATO ir koks buvo pagrindinis motyvas?
    Correct answer: Lietuva pateikė paraišką stojimui į NATO 1994 metais, siekdama užtikrinti savo saugumą po nepriklausomybės atkūrimo.
    Generated answer: Lietuva pateikė paraišką stojimui į NATO 1994 metais. Pagrindinė priežastis buvo siekis sumažinti ekonominę priklausomybę nuo Rusijos ir sustiprinti regioninę prekybą."""
},
{
    "role": "assistant",
    "content": "False: „Correct answer“ ir „Generated answer“ skiriasi. Nors data yra ta pati, pagrindinės motyvacijos nėra suderintos: pagrindinis tikslas buvo saugumo užtikrinimas, o ne ekonominės priklausomybės mažinimas."
},

{
    "role": "user",
    "content": """Question: Kokie yra keturi populiariausi muziejai Lietuvoje?
    Correct answer: Lietuvos nacionalinis muziejus, Trakų pilies muziejus, MO muziejus ir Lietuvos dailės muziejus.
    Generated answer: Lietuvos nacionalinis muziejus, Trakų pilies muziejus, MO muziejus ir Šaltojo karo muziejus."""
},
{
    "role": "assistant",
    "content": "False: „Correct answer“ ir „Generated answer“ dalijasi trimis muziejais (Lietuvos nacionalinis muziejus, Trakų pilies muziejus ir MO muziejus), tačiau „Generated answer“ neturi Lietuvos dailės muziejaus, kuris yra „Correct answer“, o vietoje jo nurodytas Šaltojo karo muziejus."
},


       {
    "role": "user",
    "content": """Question: Kada nuskendo „Meridianas“ laivas?
    Correct answer: Klaipėdoje, apie 1945 metus.
    Generated answer: 1945 metais, Kaune."""
},
{
    "role": "assistant",
    "content": "True: Klausimas yra apie datą, kada nuskendo laivas. Atsakymai sutampa dėl metų, tačiau vietos skirtumas nėra svarbus klausimui."
},
        {"role": "user", "content": PLACEHOLDER}
    ]

def lt_few_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Lithuanian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                     Start replying with True in case answers match, and False otherwise"""
    },
{
        "role": "user",
        "content": """Question: Kada Lietuva tapo Europos Sąjungos nare ir kodėl šis žingsnis buvo svarbus?
        Correct answer: Lietuva tapo Europos Sąjungos nare 2004 metų gegužės 1 dieną, siekdama užtikrinti ekonominį stabilumą, demokratiją ir saugumą.
        Generated answer: Lietuva prisijungė prie Europos Sąjungos 2004 metų pavasarį, gegužės mėnesį. Tai buvo svarbus žingsnis, kuris padėjo sustiprinti šalies ekonomiką, demokratiją ir regioninį saugumą."""
        },
        {
        "role": "assistant",
        "content": "True, „Correct answer“ ir „Generated answer“ perteikia tą pačią esmę, nurodo tą pačią datą ir priežastis."
        },


   {
    "role": "user",
    "content": """Question: Kuris lietuvių mokslininkas įkūrė pirmąją chemijos laboratoriją pasaulyje?
    Correct answer: Jonas Dagys įkūrė pirmąją chemijos laboratoriją pasaulyje XIX amžiuje.
    Generated answer: Simonas Daukantas įkūrė pirmąją chemijos laboratoriją pasaulyje XIX amžiuje."""
},
{
    "role": "assistant",
    "content": "False: Simonas Daukantas buvo istorikas, o ne chemikas. Jonas Dagys įkūrė chemijos laboratoriją ir svariai prisidėjo prie chemijos mokslo plėtros."
},


   {
    "role": "user",
    "content": """Question: Kuris lietuvių botanikas paskelbė savo darbą „Flora Lituanica“ 1753 metais?
    Correct answer: Kazimieras Būga paskelbė darbą „Flora Lituanica“ 1753 metais.
    Generated answer: 1753 metais Kazimieras Būga paskelbė savo botaninį darbą „Flora Lituanica“."""
},
{
    "role": "assistant",
    "content": "True: Atsakymas yra teisingas, nes Kazimieras Būga paskelbė šį svarbų botanikos darbą po savo kelionių po Lietuvą."
},

    {"role": "user", "content": PLACEHOLDER}

]

def lt_zero_shot(PLACEHOLDER):
    return [
    {
        "role": "system", "content": """You are provided with question, correct answer and generated answer in Lithuanian
                                     Your goal is to identify if the generated answer aligns with the correct answer (in meaning, accuracy, and relevance).
                                    Start replying with True in case answers match, and False otherwise"""
    },

    {"role": "user", "content": PLACEHOLDER}


]

def get_prompts(lang):
    if lang == "lav":
        return [
                (lav_zero_shot, "zero_shot"),
                (lav_few_shot, "few_shot"),
                (lav_few_shot_long, "few_shot_long")
                ]
    elif lang == "sw":
        return [
                (sw_zero_shot, "zero_shot"),
                (sw_few_shot, "few_shot"),
                (sw_few_shot_long, "few_shot_long"),
                ]
    elif lang == "lt":
        return [
                (lt_zero_shot, "zero_shot"),
                (lt_few_shot, "few_shot"),
                (lt_few_shot_long, "few_shot_long"),
                ]
      

