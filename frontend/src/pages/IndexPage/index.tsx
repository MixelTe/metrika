import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useHasPermission } from "../../api/operations";
import Layout from "../../components/Layout";
import { useApps, useMutationNewApp } from "../../api/app";
import Popup from "../../components/Popup";
import Spinner from "../../components/Spinner";

export default function IndexPage()
{
	const [addAppPopup, setAddAppPopup] = useState(false);
	const inp_name = useRef<HTMLInputElement>(null);
	const apps = useApps();
	const addApp = useMutationNewApp();

	return (
		<Layout centeredPage gap="1em">
			{apps.isLoading && <Spinner />}
			{addApp.isLoading && <Spinner />}
			<h1>Your Apps</h1>
			{apps.isError && `${apps.error}`}
			{apps.data?.map(v => <Link to={"/app/" + v.id}>
				<div>{v.name}</div>
				<div>{v.code}</div>
			</Link>)}
			{useHasPermission("add_app") && <button onClick={() => setAddAppPopup(true)}>Add app</button>}
			<Popup title="Add new App" open={addAppPopup} close={() => setAddAppPopup(false)}>
				<form onSubmit={e =>
				{
					e.preventDefault();
					if (!inp_name.current || inp_name.current.value == "") return;
					addApp.mutate({
						name: inp_name.current.value,
					}, {
						onSuccess: () => setAddAppPopup(false),
					});
				}}>
					{addApp.isError && `${addApp.error}`}
					<label>
						<div>Name</div>
						<input type="text" ref={inp_name} />
					</label>
					<button type="submit">Submit</button>
				</form>
			</Popup>
		</Layout>
	);
}
