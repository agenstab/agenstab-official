/**
 * AGENSTAB Example: Fill a multi-step form
 *
 * Demonstrates using fillForm() and sequential navigation
 * to complete a multi-page application form.
 */

const { BrowserAgent } = require('@agenstab/sdk');

async function main() {
    const agent = await BrowserAgent.init({
        apiKey: 'ak_live_...',
        sessionConfig: { headless: true }
    });

    try {
        await agent.navigate('https://portal.example.com/application');

        // Step 1: Personal Information
        const step1 = await agent.observe();
        console.log(`Step 1: ${step1.axtree.length} elements found`);

        await agent.fillForm({
            'a_12': 'Jane Smith',
            'a_14': 'jane@company.com',
            'a_16': '+1-555-0100'
        });

        // Find and click the "Next" button
        const nextBtn = step1.axtree.find(el => el.name === 'Next');
        await agent.click(nextBtn.agent_id);

        // Step 2: Address
        const step2 = await agent.observe();
        console.log(`Step 2: ${step2.axtree.length} elements found`);

        await agent.fillForm({
            'a_22': '123 Main St',
            'a_24': 'San Francisco',
            'a_26': 'CA'
        });

        // Submit
        const submitBtn = step2.axtree.find(el => el.name === 'Submit');
        await agent.click(submitBtn.agent_id);

        // Verify confirmation
        const confirmation = await agent.observe();
        const success = confirmation.axtree.find(el =>
            el.name && el.name.toLowerCase().includes('success')
        );

        console.log(success ? '✅ Form submitted' : '❌ Submission failed');

    } finally {
        await agent.destroy();
    }
}

main();
