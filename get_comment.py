from flask import Flask, request
from flask_cors import CORS, cross_origin
import view_comparison, topic_clustering
import openai

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = openai.OpenAI(
    api_key=""
)

def get_article_text(url):
    return requested_articles[url]

def generate_comment(articles, url):
    articles_string = "".join(
        ('article ' + str(i + 1) + ':\n' + articles[i] + '\n') for i in range(1, len(articles))
    )
    prompt = (
        "You are a journalist.\n"
        "You are given the following article:\n"
        f"{articles[0]}\n"
        "You are also given additional similar articles with different views:\n"
        f"{articles_string}\n\n"
        "Write a short summary of the information given in the additional articles, which contradicts or is not emphasized in the original\n"
        "Use a format similar to:\n"
        "'Similar articles with a different viewpoint suggest that ...'\n"
        "Keep your response short and concise (Up to two sentences)."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    source = "\n\nSource: http://rightleaningnews.com/student-loans"
    if url == "http://localhost/page2":
        source = "\n\nSource: http://rightleaningnews.com/israel-palestine"

    # Extract the response content
    return response.choices[0].message.content.strip() + source


@app.route('/get_comment')
@cross_origin()
def index():
    print("Started processing request")
    article_url = request.args.get('article')

    # Target article text and date, read from url

    similar_topic_articles = topic_clustering.cluster_and_find_target_articles(
        get_article_text(article_url),
        [article["text"] for article in articles_data],
        [article["date"] for article in articles_data],
        num_clusters=2,
    )
    adjancency_matrix = view_comparison.create_adjacency_matrix(similar_topic_articles)
    relevant_article_ids = view_comparison.find_optimal_subset(adjancency_matrix)
    relevant_articles = [similar_topic_articles[i] for i in relevant_article_ids]

    return generate_comment(relevant_articles, article_url)


articles_data = [
    {
        "text": """
        Title: "Gaza Conflict: The True Cost of Radical Ideology and the Need for Unwavering Support for Israel"

In the latest chapter of the ongoing Gaza conflict, the world once again witnesses the stark reality of a region entrenched in radical ideology and violence. The Hamas-controlled Gaza Strip stands as a testament to the failure of appeasement and the dangers of ignoring the true nature of extremism.

The Radical Ideology of Hamas

Hamas, the Islamist militant group that governs Gaza, is not just a political organization but a terrorist entity dedicated to the destruction of Israel. Founded on a radical ideology that openly calls for the annihilation of the Jewish state, Hamas perpetuates violence and chaos under the guise of a liberation movement. Its charter, which remains unchanged, explicitly denies the legitimacy of Israel and glorifies jihad against the Jewish people. This commitment to terror is evident in the relentless rocket attacks aimed at civilian populations and the indiscriminate targeting of innocent lives.

The Consequences of Weakness

The persistent violence emanating from Gaza is a direct result of a failure to address the root causes of the conflict with strength and resolve. Previous efforts at peace negotiations and ceasefires have only served to embolden Hamas, allowing them to rearm and regroup. This cycle of temporary truce followed by renewed aggression highlights the futility of half-hearted measures and the need for a firm, uncompromising stance against terrorism.

Supporting Israel: A Moral Imperative

In this context, it is imperative that the international community unequivocally supports Israel's right to defend itself. Israel, the only democratic state in the region, faces existential threats from a neighboring entity that rejects coexistence and embraces violence. The moral clarity of standing with Israel is not just about supporting a strategic ally but about endorsing the values of democracy and freedom against tyranny and oppression.

The Role of Western Nations

Western nations, especially those that champion human rights and democratic values, have a crucial role to play. They must reject any form of moral equivalence that suggests a parity between Israel’s defensive actions and the aggression of Hamas. The international community should recognize that Israel's operations in Gaza are not acts of aggression but necessary measures to safeguard its citizens from terrorism.

Conclusion: Standing Firm Against Terrorism

As the conflict continues, it is clear that only through unwavering support for Israel and a robust stance against terrorism can there be hope for a lasting peace. The world must understand that the Gaza conflict is not a simple territorial dispute but a battle between radical extremism and democratic values. Standing with Israel is not only a strategic necessity but a moral duty.
        """,
        "date": "2024-07-10"
    },
    {
        "text": """
Title: "Gaza Under Siege: The Humanitarian Crisis and the Call for Justice for Palestinians"

The Gaza Strip, a densely populated area under a brutal blockade, continues to suffer from an acute humanitarian crisis, exacerbated by ongoing conflict and international indifference. The situation in Gaza underscores the urgent need for global solidarity with the Palestinian people and a re-evaluation of policies that perpetuate their suffering.

The Humanitarian Catastrophe

For years, the people of Gaza have endured a suffocating blockade imposed by Israel, which severely restricts access to essential goods, medical supplies, and humanitarian aid. This blockade, combined with recurrent military assaults, has created a dire humanitarian situation. Hospitals are overwhelmed, and civilians face shortages of food, clean water, and basic necessities. The United Nations and numerous human rights organizations have repeatedly highlighted the severe impacts on Gaza's civilian population, yet these warnings have been met with insufficient international action.

The Legacy of Occupation and Oppression

The conflict in Gaza cannot be understood in isolation from the broader context of the Israeli occupation and the systemic oppression faced by Palestinians. Gaza’s plight is a direct consequence of decades of occupation, land dispossession, and political disenfranchisement. The international community’s failure to address the root causes of the conflict—namely, the occupation and the denial of Palestinian rights—only perpetuates the cycle of violence and suffering.

The Role of International Law

International law unequivocally supports the rights of Palestinians, including their right to self-determination and sovereignty. The United Nations has passed numerous resolutions affirming these rights and condemning the Israeli occupation. Despite this, there is a glaring disparity between legal principles and actual practices on the ground. The international community must uphold its own legal standards and pressure Israel to end its occupation and lift the blockade on Gaza.

The Urgent Need for Global Solidarity

The Palestinian people are not merely victims of conflict; they are active agents in their own struggle for justice and self-determination. Global solidarity with Palestine means more than just expressing sympathy; it involves taking concrete actions to support their rights. This includes advocating for the end of the blockade, pushing for meaningful peace negotiations that address the core issues, and holding those who violate international law accountable.

Challenging the Narrative

The dominant narratives often frame the Gaza conflict in ways that obscure the reality of Palestinian suffering and resist the call for justice. It is crucial to challenge these narratives and recognize the Palestinian struggle as a fight for fundamental human rights rather than a mere geopolitical dispute. Support for Palestine is not about opposing Israel, but about standing up for justice and human dignity.

Conclusion: A Call for Justice and Change

The situation in Gaza is a stark reminder of the urgent need for a fair and just resolution to the Israeli-Palestinian conflict. The international community must rise to the occasion, address the humanitarian crisis, and work towards a lasting peace based on justice and equality. Standing in solidarity with the people of Gaza is not only a moral imperative but a necessary step towards achieving a just and enduring resolution to the conflict.
        """,
        "date": "2024-07-10"
    },
    {
        "text": """
Title: "The Gaza Conflict: A Balanced Look at the Humanitarian and Political Dimensions"

The Gaza Strip, a densely populated area of the Middle East, remains a focal point of international concern due to its ongoing conflict and humanitarian challenges. The situation in Gaza is complex, involving historical grievances, political disputes, and humanitarian issues. This article aims to provide a balanced overview of the current state of affairs in Gaza, examining both sides of the conflict and the broader implications.

Background of the Conflict

The Gaza conflict is part of the larger Israeli-Palestinian conflict, which has deep historical roots dating back to the early 20th century. Gaza, a region governed by the Palestinian militant group Hamas since 2007, has experienced recurrent bouts of violence between Hamas and Israel. The conflict has seen multiple escalations, with both sides accusing each other of aggression and violating international norms.

Humanitarian Conditions in Gaza

The humanitarian situation in Gaza is dire, with widespread reports of shortages in essential goods, medical supplies, and infrastructure. The region has been under a blockade imposed by Israel, which restricts the flow of goods and services. This blockade, coupled with periodic military operations, has led to significant economic and social challenges for Gaza’s population. Humanitarian organizations have frequently called for increased aid and better access for relief efforts.

Political and Security Dimensions

On the political front, the Israeli government cites security concerns as the primary reason for its actions in Gaza, including military operations and the blockade. Israel argues that measures are necessary to protect its citizens from rocket attacks and other forms of aggression emanating from Gaza. Conversely, Hamas and other Palestinian factions claim that the blockade and military actions constitute collective punishment and a violation of international law.

International Reactions and Efforts

The international community has varied in its response to the Gaza conflict. Different countries and organizations offer varying levels of support or criticism based on their political perspectives and alliances. Efforts by international bodies, including the United Nations, have focused on mediating ceasefires and addressing humanitarian needs. However, achieving a lasting resolution has proven elusive due to the entrenched positions of both sides and the complexities of the broader Israeli-Palestinian conflict.

Prospects for Peace

The quest for peace in Gaza involves addressing multiple layers of the conflict. Key issues include the need for a durable ceasefire, humanitarian relief, and a political resolution that addresses the aspirations and security concerns of both Israelis and Palestinians. Dialogues and negotiations have been attempted in the past, but achieving a comprehensive and lasting agreement remains a significant challenge.

Conclusion: Seeking a Balanced Perspective

The situation in Gaza is a reminder of the complexities inherent in the Israeli-Palestinian conflict. Both humanitarian concerns and security issues are central to understanding the ongoing conflict. A balanced perspective considers the legitimate concerns of all parties involved and emphasizes the importance of dialogue and cooperation in addressing the underlying issues. The international community continues to play a role in facilitating discussions and supporting humanitarian efforts, aiming for a resolution that respects the rights and security of all individuals affected by the conflict.
        """,
        "date": "2024-07-10"
    },
    {
        "text": """
Title: "The Student Loan Crisis: A Call for Comprehensive Reform to Address Growing Inequities"

The student loan crisis in the United States has reached a tipping point, highlighting systemic flaws in the way higher education is financed and its impact on students and families. As debt levels soar and student loan borrowers face increasing financial strain, it is clear that comprehensive reform is needed to address the growing inequities in the education system.

The Burden of Student Debt

Student loan debt has become a pervasive issue, with millions of Americans grappling with the weight of loans that can total hundreds of thousands of dollars. According to recent statistics, outstanding student loan debt in the U.S. has surpassed $1.7 trillion, affecting approximately 45 million borrowers. This staggering figure represents more than just numbers—it translates into real-life struggles for individuals who are burdened with monthly payments that often exceed their ability to repay.

Inequities in Higher Education Financing

The student loan crisis disproportionately impacts marginalized communities, including low-income students and people of color. Research has shown that Black and Hispanic students are more likely to take on higher levels of debt and face greater difficulty in repaying their loans compared to their White counterparts. This disparity exacerbates existing economic inequalities and perpetuates a cycle of financial hardship.

The Failures of the Current System

The current system of student loan financing is marked by several key failures. First, the cost of higher education has skyrocketed, outpacing wage growth and inflation. As tuition fees continue to rise, students are left with no choice but to borrow more, often taking on debt that far exceeds their future earning potential. Second, the interest rates on federal student loans can be exorbitant, further inflating the total amount borrowers must repay.

The Case for Comprehensive Reform

Addressing the student loan crisis requires a multi-faceted approach to reform. Key measures include:

    Forgiveness of Student Loan Debt: Implementing broad-based student loan forgiveness would alleviate the financial burden on millions of borrowers and provide economic relief. Such policies could include partial or full cancellation of federal student loan debt, helping to eliminate the unjust financial strain on individuals who invested in their education but are now struggling to repay their loans.

    Tuition-Free Higher Education: Expanding access to free or reduced-cost higher education would prevent future students from accumulating excessive debt. By investing in public colleges and universities and offering free community college, the government can ensure that education is a right, not a privilege reserved for those who can afford it.

    Interest Rate Reforms: Reducing interest rates on federal student loans and offering income-driven repayment plans would make debt more manageable and prevent borrowers from being trapped in a cycle of escalating debt.

The Economic and Social Impact

Student loan debt has far-reaching effects on the economy and society. Borrowers often delay major life milestones such as buying homes or starting families due to financial constraints imposed by their loans. Moreover, the mental and emotional toll of student debt can contribute to overall well-being issues, highlighting the need for systemic change.

Conclusion: A Call to Action

The student loan crisis is a pressing issue that demands immediate and comprehensive reform. Addressing the systemic problems within higher education financing is not only a matter of economic fairness but also a moral imperative. By implementing policies that provide relief to borrowers and prevent future debt accumulation, we can build a more equitable and accessible education system for all.
        """,
        "date": "2024-07-10"
    },
    {
        "text": """
Title: "Student Loan Debt: Time to Reassess and Reform Without Shifting the Burden"

As the student loan debt crisis garners increasing attention, it is crucial to approach the issue with a pragmatic perspective that emphasizes personal responsibility and sustainable solutions. While the burden of student debt is undeniable, the proposed solutions often overlook key factors and could result in unintended consequences. Here’s why we need a more balanced approach to addressing student loan debt.

The Reality of Student Loan Debt

Student loan debt, currently exceeding $1.7 trillion, is a significant issue affecting millions of Americans. However, it is essential to recognize that debt is an inherent part of financing higher education and should not be viewed solely through the lens of crisis. Many borrowers successfully manage their loans and achieve positive outcomes from their investment in education.

Personal Responsibility and Financial Literacy

A critical aspect of the student loan debate is the concept of personal responsibility. Students and their families must make informed decisions when taking on debt for higher education. This includes understanding the total cost of their education, potential return on investment, and the implications of borrowing. Greater emphasis should be placed on financial literacy programs that equip students with the knowledge to make sound financial decisions and avoid excessive borrowing.

The Pitfalls of Forgiveness

Proposals for broad-based student loan forgiveness, while well-intentioned, risk creating more problems than they solve. Forgiving federal student loans would not only place a substantial financial burden on taxpayers but could also undermine the principle of personal accountability. Additionally, such measures could incentivize irresponsible borrowing behavior and fail to address the underlying issues within higher education financing.

Reforming the Education System

Instead of focusing on debt forgiveness, we should prioritize reforms that address the root causes of high education costs. Key areas for reform include:

    Increasing Transparency in College Pricing: Institutions should provide clear and detailed information about the total cost of attendance, including tuition, fees, and living expenses. Transparency will help prospective students make informed choices and plan their finances accordingly.

    Encouraging Market Competition: Promoting competition among colleges and universities can drive down costs and improve the quality of education. This can be achieved by supporting initiatives that offer alternative educational pathways, such as vocational training and online programs, which can provide valuable skills at a lower cost.

    Strengthening Repayment Plans: Improvements in existing income-driven repayment plans and refinancing options can make managing debt more manageable without resorting to broad-based forgiveness. Ensuring that repayment plans are fair and flexible can help borrowers stay on track without placing undue strain on taxpayers.

Promoting Alternative Pathways

Expanding opportunities for students to pursue alternative educational pathways, such as apprenticeships and technical certifications, can provide valuable skills and reduce reliance on traditional four-year degrees. These options often lead to successful careers without the need for substantial student debt.

Conclusion: A Balanced Approach

Addressing the student loan debt crisis requires a balanced approach that considers personal responsibility, systemic reforms, and sustainable solutions. Rather than implementing blanket forgiveness measures, we should focus on improving transparency, promoting competition, and enhancing repayment options. By taking a thoughtful and pragmatic approach, we can address the challenges of student loan debt while upholding principles of personal accountability and fiscal responsibility.
        """,
        "date": "2024-07-10"
    },
    {
        "text": """
Title: "Navigating the Student Loan Crisis: A Balanced Perspective on Solutions and Challenges"

The student loan debt crisis has become a significant issue in the United States, impacting millions of borrowers and drawing widespread attention. With outstanding student loan debt exceeding $1.7 trillion, it is clear that the problem is both complex and multifaceted. To effectively address this issue, a balanced approach that considers both the challenges and potential solutions is essential.

Understanding the Scope of the Crisis

Student loan debt has reached unprecedented levels, affecting approximately 45 million Americans. For many, the debt incurred from financing higher education becomes a significant burden, influencing their financial stability and life decisions. The high costs associated with college and university education, coupled with rising tuition fees, contribute to the accumulation of substantial debt for graduates.

Personal Responsibility and Financial Awareness

One crucial aspect of the student loan issue is personal responsibility. Prospective students and their families must make informed decisions about borrowing and financing higher education. Financial literacy plays a vital role in helping individuals understand the implications of student loans, including interest rates, repayment terms, and long-term financial impacts. Emphasizing education about financial planning and budgeting can empower students to make better choices and manage their debt more effectively.

The Debate Over Forgiveness

The debate over student loan forgiveness is highly polarized. Proponents argue that broad-based forgiveness could alleviate the financial burden on millions of borrowers, particularly those from low-income backgrounds and marginalized communities. They contend that forgiveness would also stimulate economic activity by freeing up income for other expenditures.

On the other hand, critics express concerns that forgiveness may be financially burdensome for taxpayers and could potentially incentivize excessive borrowing. There is also apprehension that blanket forgiveness might not address the root causes of rising education costs and could overlook borrowers who have already repaid their loans or avoided borrowing altogether.

Reforming the Education System

Addressing the student loan crisis requires a multifaceted approach. Key areas for potential reform include:

    Transparency in College Costs: Enhancing transparency about the true cost of college—including tuition, fees, and additional expenses—can help students and families make informed decisions and plan their finances more effectively.

    Higher Education Affordability: Exploring ways to make higher education more affordable is crucial. This could involve increasing funding for public colleges and universities, expanding access to financial aid, and considering options for tuition-free community college programs.

    Improving Repayment Options: Refining existing repayment plans to ensure they are equitable and manageable for all borrowers is important. Income-driven repayment plans and loan refinancing options can help make debt more manageable without resorting to blanket forgiveness.

Exploring Alternative Education Pathways

Increasing access to alternative education pathways, such as vocational training, apprenticeships, and online education, can provide valuable skills and reduce the need for traditional four-year degrees. These alternatives often lead to successful careers with lower associated costs.

Conclusion: Striving for Balanced Solutions

The student loan crisis is a complex issue that requires a balanced approach. While the challenges are significant, there are viable solutions that can address the problem from multiple angles. By focusing on personal responsibility, systemic reforms, and alternative educational pathways, we can work towards a more equitable and sustainable resolution to the student loan debt crisis. Collaborative efforts from policymakers, educational institutions, and the public are essential to creating a more effective and fair system for all.
        """,
        "date": "2024-07-10"
    },
    # {
    #     "text": """
    #
    #     """,
    #     "date": "2024-07-10"
    # },
    # {
    #     "text": """
    #
    #     """,
    #     "date": "2024-07-10"
    # },
]

requested_articles = {
    "http://localhost/page1": """
Title: "Student Loan Debt: Time for Progressive Reform to Address the Crisis"

The escalating student loan debt crisis in the United States has reached a critical juncture, demanding urgent and progressive reforms to address the severe financial burden on millions of borrowers. With over $1.7 trillion in outstanding student loan debt and nearly 45 million individuals affected, it is clear that the current system is failing many Americans. Comprehensive and compassionate solutions are needed to alleviate this growing crisis and promote educational equity.

The Financial Strain of Student Loan Debt

The student loan debt crisis is more than just a financial statistic; it represents a profound economic and social challenge. Many borrowers face crippling debt that influences their ability to achieve major life milestones such as buying a home, starting a family, or saving for retirement. The high cost of education, combined with rising tuition fees and exorbitant interest rates, has led to a situation where many graduates struggle to manage their debt effectively.

Inequities and Disproportionate Impact

The student loan crisis disproportionately affects marginalized communities, including low-income individuals and people of color. Studies have shown that Black and Hispanic students are more likely to accumulate higher levels of debt and face greater difficulties in repaying their loans compared to their White peers. This disparity exacerbates existing economic inequalities and perpetuates cycles of poverty.

The Case for Student Loan Forgiveness

One of the most discussed solutions to the student loan crisis is broad-based loan forgiveness. Advocates argue that forgiving federal student loan debt would provide significant relief to millions of Americans and stimulate the economy by freeing up income for other expenditures. Forgiveness would particularly benefit those who are struggling the most, including low-income borrowers and those who have been most affected by systemic inequities.

Implementing forgiveness measures could also serve as a powerful tool for addressing economic disparities. By reducing or eliminating student debt, we can help level the playing field and offer a fresh start to individuals burdened by years of financial strain.

Expanding Access to Higher Education

A fundamental aspect of addressing the student loan crisis is ensuring that higher education is accessible and affordable for everyone. This includes:

    Tuition-Free Community College: Expanding access to tuition-free community college programs would reduce the financial barrier to higher education, allowing more students to pursue their educational goals without accumulating significant debt.

    Increased Funding for Public Universities: Providing additional funding to public colleges and universities can help keep tuition costs down and make higher education more affordable for all students.

    Enhanced Financial Aid: Increasing federal financial aid and supporting need-based scholarships can provide critical support to low-income students, reducing their reliance on student loans.

Reforming the Loan System

In addition to forgiveness and increased access to education, reforming the student loan system itself is crucial. This includes:

    Reducing Interest Rates: Lowering interest rates on federal student loans would decrease the overall cost of borrowing and make it easier for borrowers to manage their debt.
    Improving Repayment Plans: Expanding and simplifying income-driven repayment plans can help borrowers manage their payments in line with their earnings, ensuring that they do not face financial hardship due to their loan obligations.

Conclusion: A Call for Progressive Action

The student loan debt crisis is a pressing issue that requires progressive reform to create a more equitable and sustainable system. By implementing comprehensive solutions such as debt forgiveness, expanding access to affordable education, and reforming the loan system, we can address the root causes of the crisis and support millions of Americans struggling under the weight of student debt. It is time for policymakers to take bold action and prioritize the financial well-being of students and graduates, fostering a more just and inclusive educational landscape.
""",
"http://localhost/page2": """
Title: "Gaza Under Siege: The Urgent Need for Global Support and Justice for Palestinians"

The humanitarian crisis in Gaza has reached alarming proportions, revealing the dire consequences of ongoing conflict and blockades. The people of Gaza, subjected to severe restrictions and relentless violence, face a critical situation that demands international solidarity and a reassessment of policies that perpetuate their suffering.

The Humanitarian Crisis in Gaza

The Gaza Strip, home to approximately two million people, is experiencing an acute humanitarian crisis exacerbated by a prolonged blockade imposed by Israel. This blockade, which has been in place since 2007, severely restricts the flow of essential goods, medical supplies, and humanitarian aid. The impact is evident in the widespread shortages of food, clean water, and medical care. Hospitals are overwhelmed, and daily life is marked by deprivation and uncertainty.

The Impact of the Blockade and Conflict

The blockade and recurring military operations have created an environment of systemic deprivation. Restrictions on the movement of people and goods have crippled Gaza's economy, leading to high unemployment rates and widespread poverty. Additionally, military escalations have resulted in significant civilian casualties, destruction of infrastructure, and the displacement of families. The international community's response has often been insufficient, failing to address the root causes of the crisis and the dire conditions faced by Gazans.

The Case for International Support and Justice

The international community must take decisive action to address the plight of the Palestinian people in Gaza. Key steps include:

    Ending the Blockade: Lifting the blockade on Gaza is essential to alleviate the humanitarian crisis. Allowing the free flow of goods, services, and humanitarian aid will help rebuild the economy, improve living conditions, and provide necessary medical care to those in need.

    Advocating for Human Rights: The international community must hold accountable those responsible for human rights violations. This includes addressing allegations of war crimes and ensuring that all parties to the conflict adhere to international humanitarian laws.

    Supporting Palestinian Rights: The recognition and support of Palestinian rights, including the right to self-determination and sovereignty, are crucial for achieving a just and lasting resolution to the conflict. Advocating for Palestinian statehood and addressing the broader issues of occupation and land rights are essential components of this effort.

The Role of the United Nations and International Organizations

The United Nations and other international organizations play a critical role in providing humanitarian aid and advocating for the rights of Palestinians. However, their efforts have often been hampered by political constraints and a lack of decisive action. Increased support and pressure on governments to act in accordance with international laws and human rights standards are needed to make a meaningful difference.

The Broader Context of the Conflict

Understanding the Gaza conflict requires acknowledging the broader context of the Israeli-Palestinian conflict, including historical grievances, occupation, and displacement. The situation in Gaza is a reflection of long-standing issues that require comprehensive and equitable solutions. Addressing the conflict’s root causes, including the end of occupation and the establishment of a viable Palestinian state, is crucial for achieving a lasting peace.

Conclusion: A Call for Solidarity and Action

The crisis in Gaza represents a profound humanitarian and moral challenge. The international community must demonstrate unwavering solidarity with the Palestinian people by advocating for an end to the blockade, supporting human rights, and working towards a just resolution to the Israeli-Palestinian conflict. The situation in Gaza is not just a regional issue but a global concern that demands immediate and sustained action to alleviate suffering and promote justice.
"""}

if __name__ == '__main__':
    app.run(debug=True)
