import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

class SearchSystray extends Component {
    static props = [];
    static template = "xyz_web.SearchSystray";
    setup() {
        super.setup();
        this.state = {
            title: _t("Search Menus and Actions"),
        }
    }
    openSearchPalette() {
        this.env.services.command.openMainPalette({
            searchValue: "/",
        });
    }
}

export const systrayItems = {
    Component: SearchSystray,
}

const systrayRegistry = registry.category("systray");
systrayRegistry.add("xyz_web.SearchSystray", systrayItems, { sequence: 1 });