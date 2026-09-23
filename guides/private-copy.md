# Create an independent private copy

Create your private copy before adding personal information. Don't use github's Fork button for your job-search workspace: forks of public repositories are public, and github doesn't let you change a fork's visibility independently. Use a new private repository that isn't part of the public fork network instead.

A local-only copy is also supported. If you don't want github hosting, download or clone the starter, keep personal files local, and don't push them anywhere. Your assistant provider may still process the files it reads.

## Ask your agent to handle setup

Use this starting request: `Read AGENTS.md and help me create an independent private copy of this repo before onboarding. Confirm the destination with me and verify its privacy before adding personal information.`

The agent should confirm your account, repository name, and permission to create and push the copy. It must not change the public source repository's visibility or promise to convert a public fork into a private one. If its tools can't create repositories, use the manual steps below. Don't bypass host restrictions or supply credentials in chat.

## With git and the github CLI

These steps start from the public starter, not an existing populated workspace. They preserve the public `main` branch history and MIT license without creating a github fork. Use a new local directory and a new, unused repository name. Replace `YOUR-USERNAME` with your github account and change `my-job-search` if you prefer another name. Authenticate the github CLI yourself before starting.

1. Clone the public starter, remove its push destination, and create an independent private repository: `git clone --branch main --single-branch https://github.com/jwbron/next-role.git my-job-search && cd my-job-search && git remote remove origin && gh repo create YOUR-USERNAME/my-job-search --private --source=. --remote=origin`
2. From that new directory, verify the destination: `gh repo view --json nameWithOwner,isPrivate,isFork,url`. Confirm the owner/name you chose, `isPrivate: true`, and `isFork: false`. Stop if any value differs or cannot be verified. No push has happened yet.
3. Push the public starter history to your verified private destination: `git push -u origin main`.
4. Open the private repository in github and confirm the Private label and intended access list. Then open the local directory in your agent and start onboarding.

The commands stop if a step fails. Inspect the actual state before retrying, don't rerun the whole chain inside an existing populated workspace. `origin` should point only to your own private repository, not the public starter or a public fork. Don't add the public source as a push destination for personal work.

## Without the github CLI

1. On github, create a new repository under your own account. Select Private. Leave the README, license, and gitignore initialization options unchecked so the repository is empty. Don't use Fork.
2. Verify the Private label, intended owner/name, and access list in the browser before pushing anything.
3. Replace `YOUR-USERNAME` and run this from a directory where `my-job-search` doesn't already exist: `git clone --branch main --single-branch https://github.com/jwbron/next-role.git my-job-search && cd my-job-search && git remote set-url origin https://github.com/YOUR-USERNAME/my-job-search.git && git push -u origin main`
4. Open the new local directory in your agent and begin onboarding. If creation, authentication, or push fails, resolve it through the supported tools without disabling hooks or changing the destination to a public repository.

## What the private repository does not back up

`private/` stays ignored by git, even in your private repository. The workspace initializer also creates `private/.gitignore`. Ordinary commits and pushes save the reusable starter and your tracked code changes, not your resume, applications, interview notes, or offers. Keep a separate private backup for those files.

Don't remove ignore rules, force-add personal files, or add them to `starter-files.json` as part of this setup. The export ZIP remains a public-starter export and excludes the private workspace. A private destination doesn't turn ignored files into tracked files, encrypt them, or remove assistant-provider and collaborator access risks. See [privacy guidance](privacy.md).

## If you already made a public fork

Don't add personal data to it or assume that deleting the fork will erase pushed history. Start a fresh independent private copy from the public starter using the steps above. Keep any existing local personal data separate until the new destination is verified, and don't push the old fork's history into the new copy if it contains private material.

If information was already pushed publicly, treat it as exposed. Deleting a file, repository, or fork may not remove other copies. Review access and remediation, and rotate any exposed credentials through their owner.

## Sources

- [Github fork visibility](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-permissions-and-visibility-of-forks): public forks stay public and cannot change visibility independently.
- [Duplicating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository): copying a repository without using a fork relationship. The steps here copy the public main branch, not a full mirror of every branch and tag.
