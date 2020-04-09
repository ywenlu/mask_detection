#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[12]:


def lowercase_exts(folder):
    for fname in os.listdir(folder):
        name, ext = os.path.splitext(fname)
        os.rename(os.path.join(folder, fname), os.path.join(folder, name + ext.lower()))


# In[ ]:


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Lower case de file extension',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'folder',
        metavar='folder',
        type=str,
        help='Path to the folder that need lowercase file extension')

    args = parser.parse_args()

    lowercase_exts(args.folder)

    print('Successfully lower case the files extensions.')

