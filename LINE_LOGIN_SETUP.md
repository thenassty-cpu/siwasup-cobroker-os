# LINE Login Setup (Siwasup Co-Broker OS)

## Step 1: Create the LINE Login channel (LINE Developers Console)
1. https://developers.line.biz/console/ → select your Provider (the same one as OA @813nyyia, so LINE user ids match)
2. **Create a new channel → LINE Login**
   - Channel type: LINE Login
   - App types: **Web app**
   - Name: `Siwasup Co-Broker OS` (no "LINE" word at the start)
3. Tab **LINE Login** → **Callback URL**:
   `https://siwasup-cobroker-os.onrender.com/api/auth/line/callback`
4. Tab **Basic settings** → copy **Channel ID** and **Channel secret**
5. Set channel status **Published** (top of the page) so non-developers can log in

## Step 2: Render environment variables
Render dashboard → siwasup-cobroker-os → Environment:

| Key | Value |
|---|---|
| `LINE_LOGIN_CHANNEL_ID` | Channel ID from step 1 |
| `LINE_LOGIN_CHANNEL_SECRET` | Channel secret from step 1 |
| `SESSION_SECRET` | any long random string (keeps sessions valid across restarts) |
| `SUPER_ADMIN_LINE_USER_IDS` | filled in Step 3 |

## Step 3: Bootstrap the first admin (Ton)
1. Open https://assets.siwasup.com/agent_registration.html and press **เชื่อม LINE** with Ton's LINE
2. Fill the form and submit; the waiting screen shows **LINE User ID** (`U` + 32 chars)
3. Put that id in `SUPER_ADMIN_LINE_USER_IDS` on Render and redeploy
4. Log in again via LINE: Ton is linked to the Tech Architect seat (SUPER TECH) and can open the admin room

## Step 4: Link the other pillars (Gool, Bua, Lily, Support)
Each person: open the registration page, connect LINE, submit the form with the **same phone number as the existing roster entry**.
Ton opens the Lobby Approval Center and approves. A pending request whose phone matches an existing member is **linked to that seat** (keeps role/permissions) instead of creating a duplicate.

## Security model
- No passwords or PINs. Identity = LINE account verified by LINE (OpenID Connect id_token verify).
- The server issues a signed 12h session token; every admin API checks the token and live membership/permissions on the server.
- Revoking a member takes effect immediately (membership is re-checked on every request).
