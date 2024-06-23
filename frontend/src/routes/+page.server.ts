import type { PageServerLoad, Actions } from './$types';
import { schema } from '$lib/schema';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { fail, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	return {
		form: await superValidate(zod(schema))
	};
};

export const actions: Actions = {
	default: async ({ request }) => {
		const form = await superValidate(request, zod(schema));

		if (!form.valid) {
			return fail(400, { form });
		}

		// Send the form to the server and retrieve the energy consumption data
		const response = await fetch('http://backend:80/entries/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form.data)
		});

		if (response.status !== 200) {
			return fail(500, { form });
		}

		const result = await response.json();

		return redirect(302, `/${result.id}`);
	}
};
