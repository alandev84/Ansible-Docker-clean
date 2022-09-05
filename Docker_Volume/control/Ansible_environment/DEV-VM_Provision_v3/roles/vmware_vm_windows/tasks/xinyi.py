import pyvmomi as vim

def del_template(si, content, template_name):
    template= None
    template= get_obj(content, [vim.VirtualMachine], template_name)
    if template:
      task_template = template.Destroy_Task()
      while task_template.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        time.sleep(1)
    else:
      print("can't find template")

def create_template_from_vm(si, content, vm_name, new_name):
    vm = None
    if vm_name:
      vm = get_obj(content, [vim.VirtualMachine], vm_name)
    
    if vm:
      if vm.runtime.powerstate==vim.VirtualMachinePowerState.poweredon:
        task_vm = vm.PowerOff()
        while task_vm.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
          time.sleep(1)
      vm.Rename(new_name)
      vm.MarkAsTemplate()
    else:
      raise SystemExit(" unable to locate VM")
