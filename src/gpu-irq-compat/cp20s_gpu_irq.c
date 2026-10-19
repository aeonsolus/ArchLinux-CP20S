// SPDX-License-Identifier: GPL-2.0
/* CP20S exact IRQ-name fix through exported OF property APIs. No IRQ changes.
 * No module_exit: property allocations stay alive until shutdown.
 */
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/of.h>
#include <linux/of_irq.h>
#include <linux/slab.h>
static int __init cp20s_gpu_irq_init(void)
{
 struct device *dev;
 struct property *old,*p;
 const char names[]="gpu\0mmu\0job";
 const char orig[]="GPU\0MMU\0JOB";
 int i,irq[3],ret=0;
 const char *upper[3]={"GPU","MMU","JOB"};
 dev=bus_find_device_by_name(&platform_bus_type,NULL,"ff320000.gpu");
 if (!dev) return -ENODEV;
 device_lock(dev);
 if (!dev->of_node || strcmp(kbasename(dev->of_node->full_name),"gpu@ff320000") ||
     !of_device_is_compatible(dev->of_node,"arm,mali-bifrost")) {ret=-ENODEV;goto done;}
 if (dev->driver) {ret=-EBUSY;goto done;}
 old=of_find_property(dev->of_node,"interrupt-names",NULL);
 if(!old || old->length!=sizeof(orig) || memcmp(old->value,orig,sizeof(orig))) {ret=-EINVAL;goto done;}
 for(i=0;i<3;i++){irq[i]=of_irq_get_byname(dev->of_node,upper[i]);if(irq[i]<=0){ret=-EINVAL;goto done;}}
 if(irq[0]==irq[1] || irq[1]==irq[2] || irq[0]==irq[2]) {ret=-EINVAL;goto done;}
 p=kzalloc(sizeof(*p),GFP_KERNEL);if(!p){ret=-ENOMEM;goto done;}
 p->name=kstrdup("interrupt-names",GFP_KERNEL);p->value=kmemdup(names,sizeof(names),GFP_KERNEL);p->length=sizeof(names);
 if(!p->name || !p->value){kfree(p->name);kfree(p->value);kfree(p);ret=-ENOMEM;goto done;}
 ret=of_remove_property(dev->of_node,old);
 if(ret){kfree(p->name);kfree(p->value);kfree(p);goto done;}
 ret=of_add_property(dev->of_node,p);
 if(ret){pr_err("cp20s_gpu_irq: failed property add %d\n",ret);goto done;}
 pr_info("cp20s_gpu_irq: lowercase names applied; IRQs unchanged %d %d %d\n",irq[0],irq[1],irq[2]);
 done: device_unlock(dev);put_device(dev);return ret;
}
module_init(cp20s_gpu_irq_init);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("CP20S exact stock GPU IRQ-name compatibility via OF property API");
