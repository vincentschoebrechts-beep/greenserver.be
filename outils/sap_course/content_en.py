# Contenu anglais de la formation « SAP from the shop floor ».
# Chaque leçon : titre, chapeau, objectifs, corps (HTML), exemple d'atelier, points clés.
# {DIAGRAM_LEVELS} et {DIAGRAM_FLOW} sont remplacés par les schémas au moment de la construction.

LANG = {
    "course_title": "SAP from the shop floor",
    "course_tag": "Free course",
    "lesson_word": "Lesson",
    "of": "of",
    "goals": "In this lesson",
    "example": "On the shop floor",
    "keys": "Key points",
    "check": "Check yourself",
    "check_intro": "Three questions on this lesson. Pick an answer to see if it is right.",
    "check_intro_annex": "Six questions on this annex. Pick an answer to see if it is right. They are not part of the final quiz.",
    "prev": "Previous",
    "next": "Next",
    "contents": "Course contents",
    "quiz": "Final quiz",
    "switch": "Français",
    "right": "Right.",
    "wrong": "Not quite.",
    "answer_is": "The answer is:",
}

HOME = {
    "title": "SAP from the shop floor, a free course",
    "description": "A free course on SAP S/4HANA for people who work with PLCs, supervision and MES: ten lessons and a final quiz.",
    "lead": "SAP S/4HANA explained to people who work with PLCs, supervision and MES. Ten short lessons in plain words, then a final quiz. Free, no account, nothing to install.",
    "disclaimer": "An independent course, not affiliated with or endorsed by SAP SE. SAP, SAP S/4HANA and the other SAP product names are trademarks of SAP SE. Screens and settings vary from one company to another: when in doubt, your own SAP system and your SAP team have the last word.",
    "who_h": "Who it is for",
    "who": "Automation engineers, maintenance and production staff, industrial IT people: anyone who knows the factory and wants to understand what SAP does with it, especially when a company moves to S/4HANA.",
    "how_h": "How it works",
    "how": [
        "Ten lessons of about fifteen minutes each, to read in order or in any order.",
        "Each lesson ends with three questions to check yourself.",
        "The final quiz draws twenty questions from a bank of one hundred: two per lesson. Your score is calculated in your browser and is not sent anywhere.",
    ],
    "lessons_h": "The ten lessons",
    "quiz_h": "Final quiz",
    "quiz_p": "Twenty questions drawn at random from the bank, two per lesson. You can take it as many times as you like: each attempt draws a new set.",
    "quiz_btn": "Take the final quiz",
    "start_btn": "Start with lesson 1",
    "more_h": "To go further",
    "more": [
        ('https://learning.sap.com/', 'learning.sap.com', ': SAP\'s own free self-paced learning journeys, some of them with access to a practice system.'),
        ('https://community.sap.com/', 'SAP Community', ': questions and answers, with a corner for beginners.'),
        ('https://api.sap.com/', 'SAP Business Accelerator Hub', ': the catalogue of SAP\'s APIs, with their documentation.'),
    ],
    "updated": "Last updated: 7 November 2026.",
}

QUIZ = {
    "title": "Final quiz, SAP from the shop floor",
    "h1": "Final quiz",
    "lead": "Twenty questions, two per lesson, drawn from a bank of one hundred. Answer them all, then check your score. Nothing is sent: everything happens in your browser.",
    "submit": "Check my answers",
    "again": "Try a new set",
    "answered": "answered",
    "score": "Your score",
    "pass": "Well done: you know the essentials of SAP seen from the shop floor.",
    "fail": "Not there yet. Read again the lessons where you missed questions, then try a new set.",
    "missing": "Some questions are still unanswered.",
    "from_lesson": "Lesson",
}

LESSONS = [
# ------------------------------------------------------------------ 1
dict(
 slug="lesson-1", check=[0, 1, 6],
 title="SAP in the factory",
 lead="What an ERP is, where SAP S/4HANA sits among the systems of a factory, and how SAP describes a company.",
 goals=["Place SAP among the levels of a factory.", "Know what SAP does, and what it does not do.", "Recognise the main organisational units: client, company code, plant, storage location."],
 body="""
<h2>An ERP, in one sentence</h2>
<p>An ERP (enterprise resource planning) keeps the whole company in one database: sales, purchasing, production, stock, maintenance, quality and accounting. When the store issues a part, the stock changes, the order's cost changes and the accounts change, all at once. SAP S/4HANA is SAP's current ERP. It follows SAP ECC, the previous generation, and runs only on SAP HANA, SAP's in-memory database. It can be installed on the company's own servers or used as a cloud service.</p>

<h2>Where SAP sits</h2>
<p>Factories are often described in levels, from the sensors at the bottom to the business systems at the top: this is the ISA-95 model. SAP lives at the top level.</p>
{DIAGRAM_LEVELS}
<p>SAP knows what must be made, from which parts, by when, and what it costs. It does not drive machines: it does not read a sensor every 10 ms, and it should never write to a PLC. Between SAP and the machines there is usually an MES (level 3) or at least a gateway.</p>

<h2>How SAP describes a company</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Unit</th><th scope="col">What it is</th><th scope="col">Example</th></tr></thead>
<tbody>
<tr><td>Client</td><td>A self-contained environment in the SAP system, with its own data.</td><td>Client 100: production</td></tr>
<tr><td>Company code</td><td>A legal entity with its own accounts.</td><td>The Belgian company</td></tr>
<tr><td>Plant</td><td>A factory or site: the unit for production, planning and stock.</td><td>Plant 1100</td></tr>
<tr><td>Storage location</td><td>A place where stock is kept inside a plant.</td><td>0001 raw materials, 0002 finished goods</td></tr>
</tbody></table></div>

<h2>The modules you will hear about</h2>
<p>SAP is still described by its historical modules: <strong>PP</strong> (production planning), <strong>MM</strong> (materials management: purchasing and stock), <strong>QM</strong> (quality management), <strong>PM</strong> (plant maintenance), <strong>SD</strong> (sales and distribution) and <strong>FI/CO</strong> (finance and controlling). In S/4HANA they are one system sharing the same data, but the abbreviations are everywhere.</p>
""",
 example="A plant with two lines making pumps is plant 1100 in SAP. Raw materials sit in storage location 0001, the line-side racks in 0003, finished pumps in 0002. The PLCs and the supervision do not know any of these numbers: the MES, or the people, make the link.",
 keys=["SAP S/4HANA is an ERP: level 4, hours and days, not milliseconds.", "It never drives machines; an MES or a gateway sits in between.", "Client, company code, plant and storage location describe the company.", "PP, MM, QM, PM, SD and FI/CO are the module names still in daily use."],
),
# ------------------------------------------------------------------ 2
dict(
 slug="lesson-2", check=[0, 3, 4],
 title="Finding your way around SAP",
 lead="The two ways of working in SAP, the transaction codes everyone uses, and the difference between master data and transactional data.",
 goals=["Tell SAP Fiori and SAP GUI apart.", "Use transaction codes and the main keyboard shortcuts.", "Distinguish master data from transactional data."],
 body="""
<h2>Two user interfaces</h2>
<p><strong>SAP Fiori</strong> is the web interface. You open the Fiori launchpad in a browser and see tiles: each tile is an app made for one task, for example confirming a production operation. Apps are role-based: a storekeeper and a planner do not see the same tiles. Fiori works on a PC and on a tablet.</p>
<p><strong>SAP GUI</strong> is the classic Windows client. Here you work with <strong>transaction codes</strong>: short codes typed in the command field at the top left. Both interfaces work on the same data, and many people use both.</p>

<h2>Transaction codes</h2>
<ul>
<li>Type the code and press Enter from the main menu, for example <code>MM03</code> to display a material.</li>
<li><code>/n</code> before the code leaves the current transaction first: <code>/nMM03</code>.</li>
<li><code>/o</code> opens the transaction in a new session (window): <code>/oMD04</code>.</li>
<li>Many codes follow the pattern create, change, display: <code>MM01</code>, <code>MM02</code>, <code>MM03</code> for materials, <code>CO01</code>, <code>CO02</code>, <code>CO03</code> for production orders. When you only want to look, use the display code: you cannot break anything.</li>
</ul>
<p>Two keys help everywhere in SAP GUI: <strong>F1</strong> explains the field where the cursor is, <strong>F4</strong> lists its possible values.</p>

<h2>Master data and transactional data</h2>
<p><strong>Master data</strong> describes things that last: materials, bills of materials, routings, work centers, suppliers, equipment. It is created once and changed rarely.</p>
<p><strong>Transactional data</strong> records events: a production order, a confirmation, a goods movement. Each event creates a <strong>document</strong> with a number, a date and a user. A goods movement, for example, creates a material document. Documents are not deleted: a mistake is corrected by a reversal, so the history stays complete.</p>

<h2>Roles and authorisations</h2>
<p>What you can see and do depends on your roles. If an app or a transaction is missing, your role probably does not include it. To learn safely, ask for display-only roles in a test or training system.</p>
""",
 example="An operator scans a production order at the end of an operation; the MES sends the confirmation to SAP. The production order is transactional data, the material and the routing it uses are master data, and the confirmation creates a new document that anyone with the right role can display.",
 keys=["Fiori: web apps by role. SAP GUI: classic client with transaction codes.", "/n opens a code in the same window, /o in a new one; 01, 02, 03 often mean create, change, display.", "F1 explains a field, F4 lists its values.", "Master data lasts; transactional data records events in numbered documents."],
),
# ------------------------------------------------------------------ 3
dict(
 slug="lesson-3", check=[0, 4, 8],
 title="Master data for production",
 lead="The material master, the bill of materials, the work center, the routing and the production version: the five records production relies on.",
 goals=["Read a material master and know its main views.", "Understand how BOM, routing and work center fit together.", "Know why the production version matters in S/4HANA."],
 body="""
<h2>The material master</h2>
<p>Every item has one material master record: raw material, semi-finished part, finished product, spare part. It is organised in <strong>views</strong> that each department fills in: basic data, purchasing, MRP, work scheduling, quality management, accounting, costing. Most views are maintained per plant, because the same part can be planned differently in two factories.</p>
<p>The <strong>material type</strong> sets which views are allowed and how stock is valued. The standard types are ROH (raw material), HALB (semi-finished), FERT (finished product), HAWA (trading goods) and ERSA (spare parts); companies often add their own.</p>

<h2>Bill of materials, work center, routing</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Record</th><th scope="col">Answers the question</th><th scope="col">Contains</th></tr></thead>
<tbody>
<tr><td>Bill of materials (BOM)</td><td>What is it made of?</td><td>Components and quantities for a base quantity of the product</td></tr>
<tr><td>Work center</td><td>Where is the work done?</td><td>A machine, line or team, with its capacity, its working times and its cost rates</td></tr>
<tr><td>Routing</td><td>How is it made?</td><td>The sequence of operations, each at a work center, with standard times for setup, machine and labour</td></tr>
</tbody></table></div>
<p>Each operation has a <strong>control key</strong>, which says for example whether it is scheduled, costed and must be confirmed, or whether it is done by a subcontractor.</p>

<h2>The production version</h2>
<p>A product may have two BOMs (two designs) or two routings (two lines). The <strong>production version</strong> says which BOM and which routing go together, for which period and which lot sizes. In S/4HANA it is mandatory for materials produced in-house: MRP finds the BOM through it. A material without a valid production version will not be planned correctly.</p>
""",
 example="The finished pump P-200 (type FERT) has a BOM with one motor, one housing and eight screws. Its routing has operation 10, assembly at work center ASSY1, and operation 20, test at work center TEST1. Production version 0001 links that BOM and that routing. The test bench at TEST1 is what the PLC and the supervision see; in SAP it is a work center with a capacity.",
 keys=["One material master per item, in views, mostly per plant.", "BOM: what it is made of. Routing: how. Work center: where.", "The control key decides how each operation is handled.", "In S/4HANA, no production version means no correct planning."],
),
# ------------------------------------------------------------------ 4
dict(
 slug="lesson-4", check=[0, 1, 8],
 title="Planning with MRP",
 lead="How SAP turns demand into proposals: what MRP calculates, the settings that drive it and the screen planners live in.",
 goals=["Understand the net requirements calculation.", "Know the outputs of MRP: planned orders and purchase requisitions.", "Read the stock/requirements list."],
 body="""
<h2>What MRP calculates</h2>
<p>MRP (material requirements planning) compares <strong>demand</strong> with <strong>supply</strong>. Demand is made of sales orders and forecasts (planned independent requirements). Supply is the stock and everything already on its way: production orders, purchase orders. What is missing is the <strong>net requirement</strong>.</p>
<p>For each missing quantity, MRP creates a proposal at the right date. For a product made in-house, it creates a <strong>planned order</strong> and explodes the BOM: the components get <strong>dependent requirements</strong>, and MRP plans them too, level after level. For a purchased part, it creates a <strong>purchase requisition</strong>, which buyers turn into a purchase order.</p>

<h2>The settings that drive it</h2>
<p>They sit in the MRP views of the material master:</p>
<ul>
<li><strong>MRP type</strong>: whether and how the material is planned (PD for MRP, VB for a manual reorder point, ND for no planning).</li>
<li><strong>Procurement type</strong>: E for in-house production, F for external procurement, X for both.</li>
<li><strong>Lot size</strong>: EX orders exactly what is missing (lot-for-lot), FX a fixed quantity, HB up to a maximum stock.</li>
<li><strong>Lead times</strong>: in-house production time, planned delivery time, goods receipt processing time. MRP schedules backwards from the date of need.</li>
</ul>

<h2>MRP Live and MD04</h2>
<p>In S/4HANA the planning run is <strong>MRP Live</strong> (<code>MD01N</code>), which runs inside the SAP HANA database and is much faster than the classic run. Planners then work in the <strong>stock/requirements list</strong> (<code>MD04</code>, or the MRP apps in Fiori): stock, requirements and receipts in date order, with exception messages when something is late or excessive.</p>
<p>When the date comes closer, a planned order is <strong>converted</strong> into a production order: the proposal becomes a real order, ready to be released.</p>
""",
 example="Customers need 100 pumps next Friday. There are 20 in stock and nothing on order; the lot size is lot-for-lot. MRP proposes a planned order for 80 pumps, scheduled back from Friday by the production time. It explodes the BOM: 80 motors, 80 housings, 640 screws. Motors are bought, so they get a purchase requisition; housings are made in-house, so they get their own planned order.",
 keys=["Net requirement = demand − stock − receipts already planned.", "In-house: planned orders, with dependent requirements for components. Bought: purchase requisitions.", "MRP type, procurement type, lot size and lead times drive the result.", "MD01N runs MRP Live; MD04 shows the live picture for one material."],
),
# ------------------------------------------------------------------ 5
dict(
 slug="lesson-5", check=[0, 4, 6],
 title="The production order",
 lead="The life of a production order from creation to closing, its statuses, and the goods movements and confirmations that the shop floor feeds.",
 goals=["Follow a production order through its statuses.", "Know when components are issued and finished goods received.", "Understand what a confirmation reports."],
 body="""
<h2>Creation and release</h2>
<p>A production order is created by converting a planned order, or by hand (<code>CO01</code>). SAP copies the <strong>operations</strong> of the routing and the <strong>components</strong> of the BOM, through the production version, and reserves the components. An availability check tells whether the parts are there.</p>
<p>The <strong>release</strong> is the moment the order may be executed: shop papers can be printed, the order can be sent to the MES, and SAP accepts goods movements and confirmations.</p>

<h2>Statuses</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Status</th><th scope="col">Meaning</th></tr></thead>
<tbody>
<tr><td><code>CRTD</code></td><td>Created: planned, not yet executable</td></tr>
<tr><td><code>REL</code></td><td>Released: can be executed</td></tr>
<tr><td><code>PCNF</code> / <code>CNF</code></td><td>Partially confirmed / confirmed</td></tr>
<tr><td><code>PDLV</code> / <code>DLV</code></td><td>Partially delivered / delivered to stock</td></tr>
<tr><td><code>TECO</code></td><td>Technically completed: no more production expected</td></tr>
<tr><td><code>CLSD</code></td><td>Closed: costs settled, nothing more can be posted</td></tr>
</tbody></table></div>

<h2>Goods issue, confirmation, goods receipt</h2>
<ol class="steps">
<li><strong>Goods issue</strong> (movement type 261): the components leave stock and are charged to the order. With <strong>backflushing</strong>, this happens automatically when the operation is confirmed.</li>
<li><strong>Confirmation</strong> (<code>CO11N</code>): for each operation, the good quantity (yield), scrap, rework and the times actually spent. A confirmation can be partial or final. <code>CO13</code> cancels one.</li>
<li><strong>Goods receipt</strong> (movement type 101): the finished products enter stock. It can be posted automatically with the confirmation of the last operation.</li>
<li><strong>Closing</strong>: the order is set to TECO, then its costs are settled to controlling, which shows the difference between planned and actual cost.</li>
</ol>
<p>To follow many orders at once, <code>COOIS</code> lists orders, operations and components with their statuses.</p>
""",
 example="A counter on the assembly line counts 82 pumps for order 1000123, and the test bench rejects 2. At the end of the shift, the MES sends a confirmation for operation 20: yield 80, scrap 2, machine time 7.5 hours. SAP backflushes the screws and motors, and posts the goods receipt of 80 pumps automatically. Nobody typed anything in SAP.",
 keys=["Operations come from the routing, components from the BOM.", "Release opens the order to confirmations and goods movements.", "261 issues components, 101 receives finished goods; backflushing automates the issue.", "A confirmation reports yield, scrap and times; TECO ends production, settlement closes the costs."],
),
# ------------------------------------------------------------------ 6
dict(
 slug="lesson-6", check=[1, 4, 5],
 title="Stock and goods movements",
 lead="How SAP records every change in stock: movement types, stock types, documents, and the transactions the store uses every day.",
 goals=["Know the most common movement types.", "Understand the three stock types.", "Find a material's stock and its movements."],
 body="""
<h2>Movement types</h2>
<p>Every change in stock is a <strong>goods movement</strong>, and every goods movement has a three-digit <strong>movement type</strong> that tells SAP what is happening and how to post it.</p>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Type</th><th scope="col">Movement</th></tr></thead>
<tbody>
<tr><td><code>101</code></td><td>Goods receipt for a purchase order or a production order</td></tr>
<tr><td><code>261</code></td><td>Goods issue to an order</td></tr>
<tr><td><code>201</code></td><td>Goods issue to a cost center (consumption without an order)</td></tr>
<tr><td><code>311</code></td><td>Transfer between storage locations, in one step</td></tr>
<tr><td><code>321</code></td><td>Release from quality inspection to unrestricted-use stock</td></tr>
<tr><td><code>551</code></td><td>Withdrawal for scrapping</td></tr>
</tbody></table></div>
<p>A movement is reversed with the matching reversal type, usually the next number: <code>102</code> reverses <code>101</code>, <code>262</code> reverses <code>261</code>.</p>

<h2>Stock types</h2>
<p>In a storage location, the same material can be in three stock types:</p>
<ul>
<li><strong>Unrestricted-use</strong>: free to be consumed or shipped.</li>
<li><strong>Quality inspection</strong>: waiting for a quality decision.</li>
<li><strong>Blocked</strong>: not to be used.</li>
</ul>

<h2>Documents and value</h2>
<p>Each goods movement creates a <strong>material document</strong>. Stock has a value, so a valued movement also creates an <strong>accounting document</strong>: logistics and finance move together. In S/4HANA, stock quantities are calculated from the material documents themselves, which are stored in one table.</p>

<h2>Daily transactions</h2>
<ul>
<li><code>MIGO</code>: post and display most goods movements.</li>
<li><code>MMBE</code>: stock overview of a material by plant, storage location and stock type.</li>
<li>Physical inventory: stock is counted and the differences are posted, so that SAP matches the shelves.</li>
</ul>
""",
 example="The storekeeper moves 50 housings from the main store (0001) to the line-side rack (0003): movement type 311. Two housings are found dented: movement type 551, scrapping. If the line-side rack is not a separate storage location in SAP, the supervision may show a full rack while SAP shows nothing there: agreeing on storage locations early saves a lot of confusion.",
 keys=["The movement type says what happens: 101 receipt, 261 issue to order, 311 transfer, 551 scrap.", "Mistakes are reversed, never deleted (102 for 101, 262 for 261).", "Unrestricted-use, quality inspection, blocked: only the first is free to use.", "MIGO posts movements, MMBE shows stock; each movement leaves a material document."],
),
# ------------------------------------------------------------------ 7
dict(
 slug="lesson-7", check=[0, 3, 5],
 title="Quality management",
 lead="Inspection lots, results and usage decisions: how SAP QM checks what comes in, what is made and what goes to stock.",
 goals=["Know what creates an inspection lot.", "Follow an inspection from results to usage decision.", "Know where shop-floor measurements fit in."],
 body="""
<h2>The inspection lot</h2>
<p>An <strong>inspection lot</strong> is a request to inspect a quantity of material. SAP creates it automatically when an event happens, and its <strong>origin</strong> says which event:</p>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Origin</th><th scope="col">Created by</th></tr></thead>
<tbody>
<tr><td><code>01</code></td><td>Goods receipt for a purchase order: incoming inspection</td></tr>
<tr><td><code>03</code></td><td>Release of a production order: in-process inspection along the operations</td></tr>
<tr><td><code>04</code></td><td>Goods receipt from production: final inspection; the goods usually wait in quality inspection stock</td></tr>
</tbody></table></div>

<h2>What to inspect</h2>
<p>The inspection plan (or the routing, for in-process inspection) lists the <strong>characteristics</strong> to check: a diameter, a pressure, a visual aspect. Characteristics used in many plans are defined once as <strong>master inspection characteristics</strong>. A sampling procedure says how many parts to check.</p>

<h2>From results to decision</h2>
<ol class="steps">
<li><strong>Results recording</strong> (<code>QE51N</code>): measured values or pass/fail for each characteristic.</li>
<li><strong>Usage decision</strong> (from the <code>QA32</code> worklist): the lot is accepted or rejected. The decision can post the stock to unrestricted-use, blocked or scrap.</li>
</ol>

<h2>When something goes wrong</h2>
<p>Problems are recorded as <strong>quality notifications</strong>. In the SAP standard, Q1 is a customer complaint, Q2 a complaint against a supplier and Q3 an internal problem. The notification collects the defects, the causes and the actions.</p>

<h2>Measurements from the floor</h2>
<p>Test benches and machines already measure. Their values can reach SAP through the MES or an interface that records results against the inspection lot. They should never be written straight into SAP's database.</p>
""",
 example="Pumps leave the test bench with a measured flow rate and pressure. The MES gathers the values per order and records them against the origin 04 inspection lot. The quality technician only looks at the lots out of tolerance, then makes the usage decision: the good pumps go to unrestricted-use stock with movement type 321, posted automatically.",
 keys=["Origin 01: supplier deliveries. 03: during production. 04: goods receipt from production.", "Characteristics say what to check; master inspection characteristics are reused across plans.", "Results recording, then usage decision, which moves the stock.", "Q1, Q2, Q3: customer, supplier and internal problems."],
),
# ------------------------------------------------------------------ 8
dict(
 slug="lesson-8", check=[1, 2, 6],
 title="Plant maintenance",
 lead="How SAP PM describes the installations, records breakdowns, plans repairs and triggers preventive maintenance, including from machine counters.",
 goals=["Tell functional locations and equipment apart.", "Follow a breakdown from notification to order.", "Understand counter-based preventive maintenance."],
 body="""
<h2>Technical objects</h2>
<p>A <strong>functional location</strong> is a place in the technical structure of the plant, organised as a tree: site, line, station. An <strong>equipment</strong> is an individual physical object, such as a pump or a motor, with its own serial number and history. It is installed at a functional location and can be moved to another one, taking its history with it.</p>

<h2>Notification and order</h2>
<ol class="steps">
<li><strong>Notification</strong> (<code>IW21</code>): someone reports a need. In the SAP standard, M1 is a maintenance request, M2 a malfunction report, M3 an activity report.</li>
<li><strong>Maintenance order</strong> (<code>IW31</code>): the work is planned, with operations, spare parts and external services. The order collects confirmations of time and the actual costs.</li>
<li><strong>Completion</strong>: the technician confirms the work, records the damage and the cause, and the order is closed.</li>
</ol>

<h2>Preventive maintenance</h2>
<p><strong>Maintenance plans</strong> create orders or notifications automatically:</p>
<ul>
<li><strong>Time-based</strong>: every three months, every year.</li>
<li><strong>Performance-based</strong> (counter-based): every 10,000 cycles, every 500 operating hours.</li>
</ul>
<p>Counters are <strong>measuring points</strong> on the equipment. Each reading creates a <strong>measurement document</strong>; when the counter reaches the next due value, the plan generates the work.</p>

<h2>A natural job for industrial IT</h2>
<p>PLCs and the supervision already count cycles and operating hours. Sending these counters to SAP as measurement documents, through the MES or an interface, replaces manual readings and lets maintenance follow the real use of each machine.</p>
""",
 example="The press on line 1 is functional location 1100-L1-PRESS; its hydraulic pump is an equipment with a counter of operating hours. Every night, an interface reads the hour counter from the supervision and posts a measurement document. At 2,000 hours, the maintenance plan creates an order to change the filter, with the filter already listed as a spare part.",
 keys=["Functional location: a place. Equipment: an object that can move between places.", "Notification (IW21) to report, order (IW31) to plan, execute and collect costs.", "Maintenance plans are time-based or counter-based.", "Measuring points and measurement documents can be fed from PLC counters."],
),
# ------------------------------------------------------------------ 9
dict(
 slug="lesson-9", check=[0, 5, 9],
 title="Batches and traceability",
 lead="Batches, serial numbers and where-used lists: how SAP answers the question every recall starts with.",
 goals=["Know what batch management brings.", "Tell backward and forward traceability apart.", "Understand why the shop floor makes or breaks traceability."],
 body="""
<h2>Batches</h2>
<p>A <strong>batch</strong> is a quantity of material made or received under the same conditions and tracked under one number. Batch management is switched on <strong>per material</strong>: only the items that need traceability carry it.</p>
<p>Batches are described by <strong>characteristics</strong> in their classification: viscosity, colour, supplier batch, and the dates that matter, such as the production date and the <strong>shelf life expiration date</strong> (SLED), which SAP can calculate from the material's shelf life.</p>

<h2>Choosing batches</h2>
<p>At goods issue, <strong>batch determination</strong> proposes which batches to take, following a strategy: FIFO (first in, first out) or FEFO (first expired, first out), and characteristic values that must match.</p>

<h2>Traceability</h2>
<ul>
<li><strong>Backward</strong>: from a product batch to the component batches, and from there to the suppliers.</li>
<li><strong>Forward</strong>: from a component batch to every product batch that used it, and to every customer who received them. This is what a recall needs.</li>
</ul>
<p>The batch where-used list and the <strong>Batch Information Cockpit</strong> (<code>BMBC</code>) show these links.</p>

<h2>Serial numbers</h2>
<p>A batch tracks a group of units. When each unit must be followed on its own, such as each pump with its own test record, SAP uses <strong>serial numbers</strong>. Batches and serial numbers can be used together.</p>

<h2>The weak link is on the floor</h2>
<p>SAP only knows the batches that were posted. If the line consumes batch B while SAP records batch A, the traceability is wrong, and nobody will notice until the day it is needed. Scanning batch labels at the line, and letting the MES post the goods issues per batch, is what makes traceability reliable.</p>
""",
 example="A supplier warns that one batch of seals is faulty. Forward traceability from that seal batch lists the three pump batches that used it, and the deliveries that shipped them. Because the line scans every seal box, the answer takes minutes and covers only the pumps really affected.",
 keys=["Batches are switched on per material and described by characteristics.", "FIFO takes the oldest batch, FEFO the one that expires first.", "Backward: what went into it. Forward: where it went.", "Traceability is only as good as the batches scanned and posted at the line."],
),
# ------------------------------------------------------------------ 10
dict(
 slug="lesson-10", check=[0, 1, 7],
 title="Connecting and securing the shop floor",
 lead="How data really travels between SAP and the machines, which channels exist, and how to keep that link from becoming a way into the plant.",
 goals=["Know the channels between SAP and the plant.", "Follow a counter on the line all the way to a confirmation in SAP.", "Apply basic security rules to the SAP link."],
 body="""
<h2>Translating between two worlds</h2>
<p>A PLC knows tags, counters and events. SAP knows orders, confirmations and goods movements. Something in between translates: an <strong>MES</strong>, a gateway or a piece of middleware.</p>
{DIAGRAM_FLOW}

<h2>The channels</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Channel</th><th scope="col">In a few words</th></tr></thead>
<tbody>
<tr><td>IDoc</td><td>SAP's format for asynchronous messages: sent, queued, processed later. <code>LOIPRO</code> is commonly used to send production orders to an MES.</td></tr>
<tr><td>BAPI over RFC</td><td>Functions in SAP that external programs call and that answer straight away, for example to post a confirmation.</td></tr>
<tr><td>OData APIs</td><td>Web services over HTTPS, documented on the SAP Business Accelerator Hub, such as the Production Order API and the Production Order Confirmation API.</td></tr>
<tr><td>SAP connectors</td><td>SAP Plant Connectivity (PCo) runs as a Windows service in the plant network and reads OPC UA servers, among others. With SAP Digital Manufacturing, SAP's cloud MES, the Production Connector plays that role.</td></tr>
</tbody></table></div>

<h2>From the counter to the confirmation</h2>
<ol class="steps">
<li>SAP releases the order and sends it to the MES (for example as a <code>LOIPRO</code> IDoc).</li>
<li>The PLC counts good and rejected parts; the MES reads the counters over OPC UA.</li>
<li>At the end of the operation, the MES posts a confirmation with yield and scrap (BAPI or OData).</li>
<li>SAP backflushes the components and posts the goods receipt.</li>
<li>Failed messages are watched: <code>BD87</code> shows IDocs by status and reprocesses them once the cause is fixed.</li>
</ol>

<h2>Securing the link</h2>
<ul>
<li><strong>Zones and conduits.</strong> In IEC 62443 terms, the office network and the plant network are separate zones, and the SAP link is a conduit between them: it passes through a DMZ, it is filtered, and it is documented.</li>
<li><strong>SAP never talks to the PLCs.</strong> It talks to the MES or the gateway; only those talk to the controllers.</li>
<li><strong>One technical user per interface.</strong> Use a system or communication user, which cannot log on interactively, with only the rights the interface needs.</li>
<li><strong>Encrypt.</strong> SNC for RFC, HTTPS for OData.</li>
<li><strong>Watch.</strong> Failed IDocs and rejected calls are often the first sign of trouble, on either side.</li>
</ul>
""",
 example="A plant connects its assembly lines to S/4HANA. The MES runs in the plant network and reads the PLCs over OPC UA. It exchanges data with SAP only through a server in the DMZ, with a dedicated communication user and SNC encryption. When the network team sees a new flow from the office network straight to a PLC, they know it is not the SAP link: that one never goes there.",
 keys=["An MES or gateway translates machine signals into business events.", "IDoc: asynchronous. BAPI/RFC: immediate. OData: HTTPS APIs. PCo and the Production Connector read OPC UA.", "Counter, MES, confirmation, backflush, goods receipt: no typing needed.", "Zones and conduits, a DMZ, dedicated technical users, encryption and monitoring."],
),
]

HOME_ANNEX = {
    "h": "Annex: moving to SAP S/4HANA",
    "p": "Optional. Why companies are moving, the three ways in, how the project runs, and a checklist for industrial IT. Not part of the final quiz.",
    "label": "Annex",
}

ANNEX = dict(
 slug="annex",
 title="Moving to SAP S/4HANA",
 lead="Optional annex: why companies are moving now, the three ways in, how such a project runs, and what industrial IT should prepare on the shop floor side.",
 goals=["Know why so many companies are moving to S/4HANA now.", "Tell a new implementation, a system conversion and a selective data transition apart.", "Prepare the shop floor side of the project: interfaces, identifiers, cutover."],
 body="""
<h2>Why now</h2>
<ul>
<li><strong>The end of SAP ECC.</strong> SAP's mainstream maintenance for ECC ends at the end of 2027. Optional extended maintenance, at a higher price, runs until the end of 2030. SAP's investment goes to S/4HANA, which SAP has committed to until at least 2040.</li>
<li><strong>One system for the group.</strong> Groups often replace local ERPs, SAP or not, with one S/4HANA template, so that every site works and reports the same way.</li>
</ul>

<h2>Three ways in</h2>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Approach</th><th scope="col">What it means</th><th scope="col">Typical case</th></tr></thead>
<tbody>
<tr><td>New implementation (greenfield)</td><td>A new S/4HANA system built on standard processes; only selected data is migrated.</td><td>The only way from a non-SAP ERP; also chosen to start clean.</td></tr>
<tr><td>System conversion (brownfield)</td><td>An existing SAP ECC system is converted to S/4HANA, with its data and settings.</td><td>A healthy ECC system, when history must be kept.</td></tr>
<tr><td>Selective data transition</td><td>A new system shell, with chosen data, companies or periods brought over.</td><td>Groups merging systems or splitting a business.</td></tr>
</tbody></table></div>

<h2>The group template</h2>
<p>In a group, a central team usually designs a <strong>global template</strong>: processes, settings and master data rules shared by all sites, then rolled out site after site. Each site adapts its local ways to the standard rather than the other way round: this is <strong>fit-to-standard</strong>. SAP also talks about a <strong>clean core</strong>: keep the SAP system as standard as possible and put company-specific extensions beside it, so that future upgrades stay easy.</p>

<h2>How the project runs</h2>
<p>Most projects follow <strong>SAP Activate</strong>, SAP's method, in six phases:</p>
<div class="table-scroll"><table>
<thead><tr><th scope="col">Phase</th><th scope="col">What happens</th></tr></thead>
<tbody>
<tr><td>Discover</td><td>Understand what S/4HANA offers and build the business case.</td></tr>
<tr><td>Prepare</td><td>Set up the team, the plan, the systems and the governance.</td></tr>
<tr><td>Explore</td><td>Fit-to-standard workshops: key users see the standard processes in a sandbox and list the real gaps.</td></tr>
<tr><td>Realize</td><td>Configure, build interfaces and extensions, run test data loads, test everything together.</td></tr>
<tr><td>Deploy</td><td>Train users, rehearse and run the cutover, go live.</td></tr>
<tr><td>Run</td><td>Hypercare right after go-live, then normal support and improvements.</td></tr>
</tbody></table></div>

<h2>Data migration</h2>
<ol class="steps">
<li><strong>Cleanse</strong> the old data: duplicates, obsolete parts, suppliers nobody uses anymore.</li>
<li><strong>Map</strong> old codes to new ones: material numbers, work centers, storage locations, units of measure.</li>
<li><strong>Load</strong> with the tools of the project, often the SAP S/4HANA Migration Cockpit, which works with one template per type of data.</li>
<li><strong>Check and sign off</strong>: business owners confirm that the loaded data is right. Several test loads come before the real one.</li>
</ol>
<p>At cutover, open items move too: open orders, open purchase orders, and the stock, usually counted just before.</p>

<h2>Checklist for industrial IT</h2>
<ul class="checklist">
<li><strong>List every flow</strong> between the old ERP and the plant: orders sent to the MES, confirmations, label printing, scanners, scales, quality results, maintenance counters. For each: direction, protocol, frequency, owner.</li>
<li><strong>Check identifiers and field lengths.</strong> Production order numbers have 12 characters in SAP; material numbers can have up to 40 in S/4HANA. MES tables, HMI fields, PLC strings and barcodes sized for the old ERP may cut them.</li>
<li><strong>Agree on storage locations and work centers</strong> with the project, so that what the floor sees matches what SAP knows.</li>
<li><strong>Rebuild the interfaces</strong> with SAP's channels (IDoc, BAPI, OData) and test them end to end in the test system, with real scanners and printers.</li>
<li><strong>Secure the new conduits</strong>: firewall rules, technical users, encryption, documentation (lesson 10).</li>
<li><strong>Plan the cutover with production</strong>: reduced output or a stop, stock count, master data freeze, and a fallback plan if go-live is postponed.</li>
<li><strong>Prepare hypercare</strong>: who to call, how interface errors are watched, how fast they are fixed.</li>
<li><strong>Train key users and operators</strong>: screens, labels and scanner steps all change.</li>
</ul>
""",
 example="A group decides to replace a site's local ERP with its S/4HANA template. Industrial IT lists fourteen flows with the plant. Testing shows that the MES expects 8-digit order numbers while SAP sends 12: the MES table and the label layouts are changed before go-live. After two test loads, the site goes live over a long weekend, right after a stock count. In the first week, thirty IDocs fail on a unit of measure mapping; hypercare fixes the mapping and reprocesses them.",
 keys=["ECC mainstream maintenance ends at the end of 2027; extended maintenance runs until 2030.", "From a non-SAP ERP: new implementation. From ECC: conversion, new implementation or selective transition.", "SAP Activate: Discover, Prepare, Explore (fit-to-standard), Realize, Deploy, Run.", "For industrial IT: list the flows, check field lengths, rebuild and test interfaces, plan cutover and hypercare."],
)
