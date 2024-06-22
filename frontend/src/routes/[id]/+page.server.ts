import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
	let response = await fetch(`http://backend:80/entries/${params.id}`);

	return response.json();
};
