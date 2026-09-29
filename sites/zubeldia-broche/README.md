# zubeldia-broche (work in progress)

This will be the automatic reply for the estimate form on https://zubeldia-broche.netlify.app.
Each time someone submits the form, it will email them back right away and send the owner a lead alert.

**Status:** Only the project setup is here (`netlify.toml`, `package.json`). The function isn't written yet.

**Still needed:**

1. The site's `index.html`, copied into `public/`. The live site was deployed by upload, so its source isn't in this repo.
2. Netlify Forms turned on for the site, and `data-netlify="true"` added to the form.
3. `netlify/functions/submission-created.mts`: the function that sends the reply email and the owner alert.
4. Email credentials stored as Netlify environment variables, for example a Gmail app password.
