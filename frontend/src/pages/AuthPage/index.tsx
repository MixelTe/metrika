import { useRef, useState } from "react";
import styles from "./styles.module.css"
import { useMutationAuth } from "../../api/auth";
import Layout from "../../components/Layout";
import { useTitle } from "../../utils/useTtile";
import Spinner from "../../components/Spinner";

export default function AuthPage()
{
	useTitle("Auth");
	const [error, setError] = useState("");
	const inp_login = useRef<HTMLInputElement>(null);
	const inp_password = useRef<HTMLInputElement>(null);
	const mutation = useMutationAuth(setError);

	function onSubmit()
	{
		const login = inp_login.current?.value || "";
		const password = inp_password.current?.value || "";
		mutation.mutate({ login, password });
	}

	return (
		<Layout header={null} centered centeredPage gap="2em">
			<h1>Metrika</h1>
			{error && <h3>{error}</h3>}
			{mutation.isLoading && <Spinner />}
			<form className={styles.form} onSubmit={e => { e.preventDefault(); onSubmit(); }}>
				<label>
					<div>Login</div>
					<input ref={inp_login} type="text" name="login" required />
				</label>
				<label>
					<div>Password</div>
					<input ref={inp_password} type="password" name="password" required />
				</label>
				<button type="submit" disabled={mutation.status == "loading"}>Log in</button>
			</form>
		</Layout>
	);
}
