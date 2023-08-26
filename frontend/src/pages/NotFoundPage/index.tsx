import HeaderBack from "../../components/HeaderBack";
import Layout from "../../components/Layout";

export default function NotFoundPage()
{
	return (
		<Layout centered header={<HeaderBack />}>
			Такой страницы нет
		</Layout>
	);
}
