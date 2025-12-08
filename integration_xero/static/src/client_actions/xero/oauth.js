import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

export function xeroOAuth(env, data) {
    const { ui, bus_service, action } = env.services
    ui.block({
        message: _t("Authenticating..."),
    })

    const authWindow = window.open('/xero/callback', '_blank');

    bus_service.addChannel('on_xero_authentication')

    bus_service.subscribe('status', (result) => {
        action.doAction('soft_reload')
        authWindow.close()
        ui.unblock()
    });

    
    console.log(env)
}


registry.category("actions").add("xero_integration.oauth", xeroOAuth);