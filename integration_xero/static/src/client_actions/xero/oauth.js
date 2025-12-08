import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

export async function xeroOAuth(env, action) {
    const { ui } = env.services
    ui.block({
        message: _t("Authenticating..."),
    })

    window.open('/xero/callback', '_blank');

    env.bus.addEventListener("on_xero_aunthentication", (x) => {
        console.log(x)
        console.log(env)
        console.log(action)
        ui.unblock()
    });
}


registry.category("actions").add("xero_integration.oauth", xeroOAuth);