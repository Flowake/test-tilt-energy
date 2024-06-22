import { z } from 'zod';

export const appliances = {
	fridge: 'Fridge',
	freezer: 'Freezer',
	washing_machine: 'Washing machine',
	dishwasher: 'Dishwasher',
	induction_stove: 'Induction stove',
	tv: 'Television',
	small_light: 'Small light',
	big_light: 'Big light'
} as const;

type Appliances = keyof typeof appliances;

function applianceToMinimumKiloWattHours(appliance: Appliances) {
	switch (appliance) {
		case 'fridge':
			return 2.0 * 6;
		case 'freezer':
			return 2.5 * 6;
		case 'washing_machine':
			return 1.5 * 1;
		case 'dishwasher':
			return 2.5 * 1;
		case 'induction_stove':
			return 3.0 * 1;
		case 'tv':
			return 0.5 * 4;
		case 'small_light':
			return 0.1 * 4;
		case 'big_light':
			return 0.8 * 4;
	}
}

export const schema = z
	.object({
		email: z.string().email('Please enter a valid email.'),
		appliances: z
			.array(z.enum(Object.keys(appliances) as [Appliances, ...Appliances[]]))
			.nonempty('Please select at least one appliance.'),
		total_consumption: z.coerce
			.number()
			.positive('Please enter a positive number.')
			.max(75, 'Total consumption should be less than 75 kWh.')
	})
	.superRefine(({ appliances, total_consumption }, ctx) => {
		const minimumWattHours = appliances.reduce(
			(acc, appliance) => acc + applianceToMinimumKiloWattHours(appliance),
			0
		);
		if (total_consumption < minimumWattHours) {
			ctx.addIssue({
				code: 'custom',
				message:
					'Total consumption is too low for the selected appliances. It should be at least ' +
					minimumWattHours +
					'kWh.',
				path: ['total_consumption']
			});
		}
	});