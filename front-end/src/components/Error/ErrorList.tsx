export const errors = {
  '401': {
    title: 'Sorry, we can’t show you this page.',
    description:
      'You don’t have permissions to access this page. If you believe you are seeing this in error or need additional assistance, please contact an administrator for help.',
    mailbox: '',
    errorType: 'Permissions'
  },

  '500': {
    title: 'Something went wrong.',
    description:
      'There is a problem showing this page. Please try reloading the page to see if that fixes the problem. If you need additional assistance, please contact an administrator for help.',
    mailbox: '',
    errorType: '500'
  }
}

export const notFoundErrors = {
  account: {
    title: 'The account doesn’t exist.',
    description:
      'We can’t find the account you’re looking for. If you believe you are seeing this in error, double check that the URL is correct. If you need additional assistance, please contact an admin for help.'
  },

  event: {
    title: 'The page doesn’t exist.',
    description:
      'We can’t find the page you’re looking for. If you believe you are seeing this in error, double check that the URL is correct. If you need additional assistance, please contact an admin for help.'
  },

  evaluator: {
    title: 'The results for this evaluator don’t exist.',
    description:
      'We can’t find results for this evaluator. If you believe you are seeing this in error, double check that the URL is correct. If you need additional assistance, please contact an admin for help.'
  }
}
