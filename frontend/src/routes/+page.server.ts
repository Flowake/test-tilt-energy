import type { PageServerLoad, Actions } from './$types';
import { schema } from '$lib/schema';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { message } from 'sveltekit-superforms';
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
		let response = await fetch('backend:80', {
			method: 'POST',
			body: JSON.stringify(form.data)
		});

		if (response.status !== 200) {
			return fail(500, { form });
		}

		return message(form, 'Form posted successfully!');
	}
};
