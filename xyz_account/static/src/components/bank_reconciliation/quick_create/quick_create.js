import {
    KanbanRecordQuickCreate,
    KanbanQuickCreateController,
} from "@web/views/kanban/kanban_record_quick_create";

export class BankRecQuickCreateController extends KanbanQuickCreateController {
    static template = "xyz_account.BankRecQuickCreateController";
}

export class BankRecQuickCreate extends KanbanRecordQuickCreate {
    static template = "xyz_account.BankRecQuickCreate";
    static props = {
        ...KanbanRecordQuickCreate.props,
        resModel: { type: String },
        context: { type: Object },
        group: { type: Object, optional: true },
    };
    static components = { BankRecQuickCreateController };

    /**
    Overriden.
    **/
    async getQuickCreateProps(props) {
        await super.getQuickCreateProps({
            ...props,
            group: {
                resModel: props.resModel,
                context: props.context,
            },
        });
    }
}
