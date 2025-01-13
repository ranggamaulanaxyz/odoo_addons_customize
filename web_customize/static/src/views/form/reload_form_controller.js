import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { redirect } from "@web/core/utils/urls";
export class ReloadFormController extends FormController {
    async save({ closable, ...otherParams }) {
      const saved = await super.save(otherParams);
      if ( saved && this.model.root._values.key=='web.base.sorturl'){
        redirect("/")
      }else{
        return saved;
      }
  }}

export const ReloadFormView = {
    ...formView,
    Controller: ReloadFormController,
};
registry.category("views").add("web_url_view_ir_config_inherit_form", ReloadFormView);
