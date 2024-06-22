<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { Field, Control, Label, Description, FieldErrors } from 'formsnap';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types.js';
	import { schema, Appliances, type AppliancesType } from '$lib/schema';
	import { formatApplianceName } from '$lib/helpers';

	export let data: PageData;

	let applianceSelect: AppliancesType;

	function addAppliance(appliance: AppliancesType) {
		$formData.appliances = [...$formData.appliances, appliance];
	}

	function removeAppliance(appliance: AppliancesType) {
		let index = $formData.appliances.indexOf(appliance);
		if (index !== -1) {
			$formData.appliances = [
				...$formData.appliances.slice(0, index),
				...$formData.appliances.slice(index + 1)
			];
		}
	}

	const form = superForm(data.form, {
		validators: zodClient(schema),
		dataType: 'json'
	});
	const { form: formData, enhance } = form;
</script>

<form method="POST" use:enhance>
	<Field {form} name="email">
		<Control let:attrs>
			<Label>Email</Label>
			<input {...attrs} type="email" bind:value={$formData.email} />
		</Control>
		<FieldErrors />
	</Field>
	<Field {form} name="total_consumption">
		<Control let:attrs>
			<Label>Total consumption (kWh)</Label>
			<input {...attrs} type="number" max="75" bind:value={$formData.total_consumption} />
		</Control>
		<Description>The total consumption in kWh per day of your household</Description>
		<FieldErrors />
	</Field>
	<Field {form} name="appliances">
		<Description>Select your appliances</Description>
		<select id="appliance" bind:this={applianceSelect}>
			{#each Appliances as appliance}
				<option value={appliance}>{formatApplianceName(appliance)}</option>
			{/each}
		</select>
		<button type="button" on:click={() => addAppliance(applianceSelect.value)}>Add</button>
		<ul>
			{#each $formData.appliances as appliance}
				<li>
					{formatApplianceName(appliance)}
					<button type="button" on:click={() => removeAppliance(appliance)}>Remove</button>
				</li>
			{/each}
		</ul>
		<FieldErrors />
	</Field>
	<button type="submit">Submit</button>
</form>
