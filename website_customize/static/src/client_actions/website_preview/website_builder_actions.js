import { patch } from "@web/core/utils/patch";
import { WebsiteBuilderClientAction } from "@website/client_actions/website_preview/website_builder_action";
import { getActiveHotkey } from "@web/core/hotkeys/hotkey_service";
import { redirect } from "@web/core/utils/urls";

patch(WebsiteBuilderClientAction.prototype, {
    /**
     * Handles refreshing while the website preview is active.
     * Makes it possible to stay in the backend after an F5 or CTRL-R keypress.
     * Cannot be done through the hotkey service due to F5.
     *
     * @param {KeyboardEvent} ev
     */
    onKeydownRefresh(ev) {
        const hotkey = getActiveHotkey(ev);
        if (hotkey !== "control+r" && hotkey !== "f5") {
            return;
        }
        // The iframe isn't loaded yet: fallback to default refresh.
        if (this.websiteService.contentWindow === undefined) {
            return;
        }
        ev.preventDefault();
        const path = this.websiteService.contentWindow.location;
        const debugMode = this.env.debug ? `&debug=${this.env.debug}` : "";
        redirect(
            `/app/action-website.website_preview?path=${encodeURIComponent(path)}${debugMode}`
        );
    },
    reloadWebClient() {
        const currentPath = encodeURIComponent(window.location.pathname);
        const websiteId = this.websiteService.currentWebsite.id;
        redirect(
            `/app/action-website.website_preview?website_id=${encodeURIComponent(
                websiteId
            )}&path=${currentPath}&enable_editor=1`
        );
    }
});