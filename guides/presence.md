# Personal site, writing, and LinkedIn

A small public presence gives a reviewer one place to check what the candidate does, see a few results in context, and read how they think. It supports applications and conversations, it doesn't replace them. The candidate decides what becomes public, and nothing is published, pushed, or posted without their explicit approval of the exact change.

## Why a site helps

A resume compresses work into lines. A site can add the context a recruiter or hiring manager wants after a first read: the problems the candidate is good at, a couple of results with enough detail to be believable, and writing that shows judgment. It also gives every application, profile, and follow-up a stable link the candidate controls.

A site isn't required. If the candidate has no time or no material to share yet, a consistent resume and LinkedIn profile are enough. Don't create one just because this guide exists.

## Build a minimal static site

Plain HTML and CSS are enough, and they keep the site fast, portable, and easy to review in a diff. Free static hosts such as GitHub Pages serve a repository's files directly. A custom domain is optional. If the candidate adds one, enable HTTPS in the host's settings and confirm that the certificate is active before linking the domain anywhere.

Keep the site in its own repository, not inside the private job-search copy. A public site repository should contain only content meant to be public, and its history is public too. Draft essays and plans in the private workspace under `presence/` until the candidate approves them.

A useful first version fits on one page:

- One clear positioning statement: the kind of work the candidate does and for whom, in a sentence a stranger can repeat.
- What they can do for a team: two to four specific capabilities, phrased as outcomes rather than adjectives.
- A few concrete results: short entries with the problem, the candidate's part, and what changed, drawn from confirmed evidence in `profile/career.md`.
- Writing: links to essays, once any exist.
- Contact: an email address or form, and links to LinkedIn and GitHub if the candidate uses them.

Keep the design restrained. A readable type size, generous line height, enough contrast, a narrow text column, and working layout on a phone matter more than visual flourishes. The design should get out of the way of the content, not compete with it. Check the page with a screen reader or accessibility checker when one is available, and add alt text to any image.

## Resume on the site

Offering a resume PDF saves a reviewer a step. A public copy shouldn't include a phone number, since anything on a public page can be scraped. The simplest route is a base resume whose contact line uses email and the site, which is enough for first contact. If the candidate wants a phone number on applications, keep the public copy as a separate reviewed file outside the manifest. The validator treats a different contact line as identity drift, so check the public copy's text against the base by hand before each publish.

## Keep claims consistent

The site, resume, LinkedIn, and applications should describe the same titles, dates, ownership, and results. A reviewer who sees a bigger claim in one place than another will trust all of them less. Build site copy from the same confirmed evidence as the resume, and when a fact changes, update every public surface together. Before any publish, compare the site's claims line by line with the current base resume and list any differences for the candidate.

## Turn your work into essays

A short series of essays, often three to five, lets the candidate show how they approach problems. Good topics come from work they actually did: a decision with a real tradeoff, a migration or launch and what it taught them, a debugging approach, a pattern they use with teams. Each essay should make one point, open with the problem or the conclusion, and stay short enough to read in a few minutes.

Run a confidentiality check on every draft before it goes further. Remove a former employer's internal system or project names, private metrics, incident details, customer names, colleagues' names or actions, and anything unreleased, unless the candidate has permission to share it. Generalize instead: "a payments service handling peak seasonal load" rather than an internal codename and a real traffic figure. When in doubt, leave it out and ask.

The voice has to stay the candidate's. An agent can help outline, find the strongest example, and tighten a draft, but the candidate should supply the substance and the opinions. Do a review pass where the candidate reads the whole essay aloud and marks anything that doesn't sound like them or that they wouldn't defend in an interview. Don't attribute a belief or lesson to them that they haven't stated. Use `profile/voice.md` as the reference, not the agent's default style.

## Unlisted pages

Some material is useful one-to-one but not for everyone: a project deep dive for a specific interview loop, a longer case study, or a portfolio piece with more detail than the main site. An unlisted page is a page that isn't linked from the site's navigation or sitemap and carries a `<meta name="robots" content="noindex">` tag so search engines don't list it.

Unlisted isn't private. Anyone with the link can open and forward it, the file is in the public site repository and its history, and a crawler can still find it through a stray link. Apply the same confidentiality check as a public essay. Anything that genuinely must stay restricted belongs in a private document shared with specific people, not on the site.

## Where to link the site

- Application forms: the website or portfolio field.
- LinkedIn: the website field in contact info, and a Featured item for the site or a strong essay.
- GitHub: the profile's website field and, if the candidate uses one, the profile README.
- Email signature: a single plain link.
- Follow-up notes after a conversation: one relevant essay or case study that connects to what was discussed, not the whole site.

## LinkedIn

Recruiters search LinkedIn by keywords, so the profile should use the terms that accurately describe the candidate's work. Everything on it should match the resume and site.

- Headline: lead with the role and the two or three keywords a recruiter would search for, then one credential or proof point the candidate can support. For example, a fictional "Backend engineer, payments and reliability, built a ledger used by four product teams" says more than a slogan.
- About: a short version of the site's positioning statement and capabilities, in the same voice. Don't introduce claims the resume can't support.
- Experience: titles, employers, and dates should match the resume exactly. Entries can carry two or three of the same confirmed results.
- Featured: the site, one or two essays, or a public project.
- Contact info: the site in the website field.

Open to Work has a real tradeoff. The public banner tells anyone who views the profile, including a current employer, that the candidate is looking. Between jobs that's often reasonable and can bring inbound messages, though some candidates prefer not to show it. While employed, the recruiter-only setting matters most, since it signals availability to recruiters without the public banner. Recruiter-only visibility reduces exposure but isn't a guarantee that nobody at the current employer sees it. Present both options and let the candidate choose.

The agent drafts profile text for the candidate to paste. It never logs in, edits the profile, posts, comments, or messages on the candidate's behalf.

## Approval before publishing

Show the candidate the exact diff or rendered page for every change before it leaves their machine. Push, deploy, or publish only after they explicitly approve that version. Approval of an earlier version doesn't cover later edits. Preview locally first, for example with a simple local static server, and confirm what will be public. After publishing, check the live page and record the date and what changed in `presence/`.
