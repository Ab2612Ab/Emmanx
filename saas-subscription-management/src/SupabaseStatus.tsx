import { useEffect, useState } from "react";
import { supabase } from "./lib/supabase";

export function SupabaseStatus(){
  const [status,setStatus]=useState("Connecting…");
  const [counts,setCounts]=useState({plans:0,customers:0,subscriptions:0,invoices:0});
  useEffect(()=>{
    let active=true;
    (async()=>{
      const [plans,customers,subscriptions,invoices]=await Promise.all([
        supabase.from("subscription_plans").select("id",{count:"exact",head:true}),
        supabase.from("customers").select("id",{count:"exact",head:true}),
        supabase.from("subscriptions").select("id",{count:"exact",head:true}),
        supabase.from("invoices").select("id",{count:"exact",head:true})
      ]);
      if(!active)return;
      const error=plans.error||customers.error||subscriptions.error||invoices.error;
      if(error){setStatus("Supabase connection error");console.error(error);return}
      setCounts({plans:plans.count||0,customers:customers.count||0,subscriptions:subscriptions.count||0,invoices:invoices.count||0});
      setStatus("Supabase connected");
    })();
    return()=>{active=false};
  },[]);
  return <div style={{padding:"8px 24px",fontSize:12,background:"#f3faf6",borderBottom:"1px solid #dcefe4",color:"#176b4b"}}>{status} · {counts.subscriptions} subscriptions · {counts.customers} customers · {counts.plans} plans · {counts.invoices} invoices</div>
}
