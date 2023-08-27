import { useParams } from "react-router-dom";
import styles from "./styles.module.css"
import Layout from "../../components/Layout";
import { useApp } from "../../api/app";
import Spinner from "../../components/Spinner";

export default function AppPage()
{
	const appId = useParams()["appId"]!;
	const app = useApp(appId);

	return (
		<Layout centeredPage gap="1em" backLink="/">
			{app.isLoading && <Spinner />}
			{app.isError && `${app.error}`}
			<h1>{app.data?.name}</h1>
		</Layout>
	);
}
