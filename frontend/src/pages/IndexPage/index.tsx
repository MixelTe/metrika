import { Link } from "react-router-dom";
import { useHasPermission } from "../../api/operations";
import Layout from "../../components/Layout";

export default function IndexPage()
{
	return (
		<Layout centered gap="1em">
			{useHasPermission("view") && <Link to="/">Index</Link>}
		</Layout>
	);
}
